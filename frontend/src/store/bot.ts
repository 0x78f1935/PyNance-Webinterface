import { Module } from "vuex";
import axios from 'axios';

const botModule: Module<any, any> = { 
    state: {
        online: false,
        graph_type: '',
        graph_type_choices: ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'],
        graph_interval: 0
    },

    getters: {
        online: state => state.online,
        graph_type: state=>state.graph_type,
        graph_type_choices: state=>state.graph_type_choices,
        graph_interval: state=>state.graph_interval,
    },

    mutations: {
        SET_ONLINE(state, value) { state.online = value; },
        SET_GRAPH_TYPE(state, value) { state.graph_type = value; },
        SET_GRAPH_INTERVAL(state, value) { state.graph_interval = value; },
    },

    actions: {
        toggleOnline({ commit, getters }, data) {
          axios.post(`/api/v1/logic/toggle`, {'online': data}, {headers: {'token': localStorage['sk']}}).then(response => {
            commit('SET_ONLINE', response.data.online);
          });
        },
        getOnlineStatus({ commit, getters }){
            axios.get(`/api/v1/logic/toggle`, {headers: {'token': localStorage['sk']}}).then(response => {
                commit('SET_ONLINE', response.data.online);
            });
        },
        setGraph(state, value) {
            axios.post(`/api/v1/klines/graph`, {
                'graph-type': value['graph-type'],
                'graph-interval': value['graph-interval'],
            }, {headers: {'token': state.getters.token}}).then(response => {
                state.commit('SET_GRAPH_TYPE', response.data["graph-type"]);
                state.commit('SET_GRAPH_INTERVAL', response.data["graph-interval"]);
            });
        },
        getGraphInterval(state) {
            axios.get(`/api/v1/klines/graph`, {headers: {'token': state.getters.token}}).then(response => {
                state.commit('SET_GRAPH_TYPE', response.data["graph-type"]);
                state.commit('SET_GRAPH_INTERVAL', response.data["graph-interval"]);
            });
        },
    }
}

export default botModule;
