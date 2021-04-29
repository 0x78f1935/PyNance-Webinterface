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
        setOnline({ commit, getters }, data) {
          axios.post(`/api/v1/system/`, {'online': data}, {headers: {'token': getters.token}}).then(response => {
            commit('SET_ONLINE', response.data.online);
          });
        },
    }
}

export default botModule;
