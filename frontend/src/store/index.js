import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    darkmode: true,
    symbol: "LTCBTC",
    metrics: "EUR",
    symbols: [],
    candlesticks: []
  },
  getters: {
    darkmode: state => { return state.darkmode; },
    metrics: state => { return state.metrics; },
    symbol: state => { return state.symbol; },
    symbols: state => { return state.symbols; },
    candlesticks: state => { return state.candlesticks; }
  },
  mutations: {
    SET_DARKMODE(state, value) { state.darkmode = value; },
    SET_METRICS(state, value) { state.metrics = value},
    SET_SYMBOL(state, value) { state.symbol = value;},
    SET_SYMBOLS(state, value) { state.symbols = value;},
    SET_CANDLESTICKS(state, value) { state.candlesticks = value; },
  },
  actions: {
    get_symbols({ commit }, format) {
      axios.get(`/api/v1/symbols/?format=${format}`).then(response => {
        commit('SET_SYMBOLS', response.data);
      })
    },
    get_candlesticks(state) {
      axios.get(`/api/v1/candlesticks/?symbol=${state.getters.symbol}`).then(response => {
        state.commit('SET_CANDLESTICKS', response.data);
      })
    }
  },
  modules: {
  }
})
