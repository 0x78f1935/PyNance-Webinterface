import { Module } from "vuex";
import axios from 'axios';

const botModule: Module<any, any> = { 
    state: {
        online: false,
    },

    getters: {
        online: state => state.online,
    },

    mutations: {
        SET_ONLINE(state, value) { state.online = value; },
    },

    actions: {
        toggleOnline({ commit, getters }, data) {
          axios.post(`/api/v1/logic/toggle`, {'online': data}, {headers: {'token': getters.token}}).then(response => {
            commit('SET_ONLINE', response.data.online);
          });
        },
        getOnlineStatus({ commit, getters }){
            axios.get(`/api/v1/logic/toggle`, {headers: {'token': getters.token}}).then(response => {
                commit('SET_ONLINE', response.data.online);
            });
        }
    }
}

export default botModule;
