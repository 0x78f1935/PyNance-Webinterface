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
}

export default keysModule;
