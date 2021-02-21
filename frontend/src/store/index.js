import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    darkmode: false,
    symbol: "BTC",
    symbols: [],
  },
  getters: {
    darkmode: state => { return state.darkmode; },
    symbol: state => { return state.symbol; },
    symbols: state => { return state.symbols; },
  },
  mutations: {
    SET_DARKMODE(state, value) { state.darkmode = value; },
    SET_SYMBOL(state, value) { state.symbol = value;},
    SET_SYMBOLS(state, value) { state.symbols = value;},
  },
  actions: {
    get_symbols({ commit }, format) {
      axios.get(`/api/v1/symbols/?format=${format}`).then(response => {
        commit('SET_SYMBOLS', response.data);
      })
    },

  },
  modules: {
  }
})
