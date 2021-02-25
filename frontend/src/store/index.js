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
    candlesticks: [],
    total_balance_1: {asset: '', value: '0', free: '', locked: ''},
    total_balance_2: {asset: '', value: '0', free: '', locked: ''},
  },
  getters: {
    darkmode: state => { return state.darkmode; },
    metrics: state => { return state.metrics; },
    symbol: state => { return state.symbol; },
    symbols: state => { return state.symbols; },
    candlesticks: state => { return state.candlesticks; },
    total_balance_1: state => { return state.total_balance_1; },
    total_balance_2: state => { return state.total_balance_2; },
  },
  mutations: {
    SET_DARKMODE(state, value) { state.darkmode = value; },
    SET_METRICS(state, value) { state.metrics = value},
    SET_SYMBOL(state, value) { state.symbol = value;},
    SET_SYMBOLS(state, value) { state.symbols = value;},
    SET_CANDLESTICKS(state, value) { state.candlesticks = value; },
    SET_TOTAL_BALANCE_1(state, value) { 
      state.total_balance_1.asset = value.asset;
      state.total_balance_1.value = value.total; 
      state.total_balance_1.free = value.free; 
      state.total_balance_1.locked = value.locked; 
    },
    SET_TOTAL_BALANCE_2(state, value) { 
      state.total_balance_2.asset = value.asset;
      state.total_balance_2.value = value.total; 
      state.total_balance_2.free = value.free; 
      state.total_balance_2.locked = value.locked; 
    },
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
    },
    get_total_balance(state){
      axios.get(`/api/v1/balance/?format=live&option=${state.getters.symbol}`).then(response => {
        // console.log(response.data)
        state.commit('SET_TOTAL_BALANCE_1', response.data.shift(0));
        state.commit('SET_TOTAL_BALANCE_2', response.data.shift(1));
      })
    }
  },
  modules: {
  }
})
