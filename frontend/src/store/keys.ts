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
        coinmarketcal(state, value) { state.coinmarketcal = value; },
    },

    actions: {
        loadKeys(state) {
            if(state.getters.authenticated){
                axios.get(`/api/v1/keys/`, {headers: {'token': state.getters.token}}).then(response => {
                    response.data.forEach(element => {
                        for (const [key, value] of Object.entries(element)) {
                            state.commit(key, value);
                            // console.log(`${key}: ${value}`);
                        }
                    });
                });
            }
        }
    }
}

export default keysModule;
