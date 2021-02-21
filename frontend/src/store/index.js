import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    darkmode: false,
    symbol: "LTCBTC"
  },
  getters: {
    darkmode: state => { return state.darkmode; },
    symbol: state => { return state.symbol; }
  },
  mutations: {
    toggle_darkmode(state) { state.darkmode = !state.darkmode; },
    set_symbol(state, value) { state.symbol = value;}
  },
  actions: {
  },
  modules: {
  }
})
