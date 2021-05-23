import { Module } from "vuex";
import axios from 'axios';

const PricesModule: Module<any, any> = { 
    state: {
        prices: [],
    },

    getters: {
        prices: state => state.prices,
    },

    mutations: {
        SET_PRICES(state, value) { state.prices = value; },
    },

    actions: {
        fetchPrices(state){
            axios.get(`/api/v1/prices`, {headers: {'token': state.getters.token}}).then(response => {
                state.commit('SET_PRICES', response.data);
            })
        }
    }
}

export default PricesModule;
