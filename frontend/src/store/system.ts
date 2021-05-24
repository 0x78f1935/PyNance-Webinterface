import { Module } from "vuex";
import axios from 'axios';

const systemModule: Module<any, any> = { 
    state: {
        version: 'x.x.x',
        language: 'en',
        tos: false,
        authentication: false,
        authenticated: false,
        token: '',
    },

    getters: {
        version: state => state.version,
        language: state => state.language,
        tos: state => state.tos,
        authentication: state => state.authentication,
        authenticated: state => state.authenticated,
        token: state => state.token,
    },

    mutations: {
        SET_VERSION(state, value) { state.version = value; },
        SET_LANGUAGE(state, value) { state.language = value; },
        SET_TOS(state, value) { state.tos = value; },
        SET_AUTHENTICATION(state, value) { state.authentication = value; },
        SET_AUTHENTICATED(state, value) { state.authenticated = value; },
        SET_TOKEN(state, value) { state.token = value; },
    },

    actions: {
        loadDashboard(state) {
            axios.get(`/api/v1/system/`, {headers: {'token': localStorage['sk']}}).then(response => {
                state.commit('SET_VERSION', response.data.version);
                state.commit('SET_LANGUAGE', response.data.language);
                state.commit('SET_TOS', response.data.tos);
                state.commit('SET_AUTHENTICATION', response.data.authentication);
                state.commit('SET_TOKEN', response.data.token);
            });
        }
    }
}

export default systemModule;
