import { Module } from "vuex";
import axios from 'axios';

const keysModule: Module<any, any> = { 
    state: {
        coinmarketcal: '',
    },

    getters: {
        coinmarketcal: state => state.coinmarketcal,
    },

    mutations: {
        SET_CONMARKETCAL(state, value) { state.coinmarketcal = value; },
    },

    actions: {
        setCoinmarketcal({ commit, getters }, data) {
          axios.post(`/api/v1/system/`, {'online': data}, {headers: {'token': getters.token}}).then(response => {
            commit('SET_ONLINE', response.data.online);
          });
        },
    }
}

export default keysModule;
