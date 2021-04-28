import { Module } from "vuex";
import axios from 'axios';

const systemModule: Module<any, any> = { 
    state: {
        online: false,
        version: 'x.x.x',
    },

    getters: {
        online: state => state.online,
        version: state => state.version,
    },

    mutations: {
        SET_ONLINE(state, value) { state.online = value; },
        SET_VERSION(state, value) { state.version = value; },
    },

    actions: {
        setOnline({ commit, getters }, data) {
          axios.post(`/api/v1/system/`, {'online': data}, {headers: {'token': getters.token}}).then(response => {
            commit('SET_ONLINE', response.data.online);
          });
        },
    }
}

export default systemModule;
