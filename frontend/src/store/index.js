import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    darkmode: true,
    chatterer: "",
    online: false,
    take_profit: 0,
    symbols: [],
    symbols_sets: [],
    cur1: "",
    cur2: "",
    drawer: true,
    panik: false,
  },
  getters: {
    darkmode: state => { return state.darkmode; },
    chatterer: state => { return state.chatterer; },
    online: state => { return state.online; },
    take_profit: state => { return state.take_profit; },
    symbols: state => { return state.symbols; },
    symbols_sets: state => { return state.symbols_sets; },
    cur1: state => { return state.cur1; },
    cur2: state => { return state.cur2; },
    drawer: state => { return state.drawer; },
    panik: state => { return state.panik; },
  },
  mutations: {
    SET_DARKMODE(state, value) { state.darkmode = value; },
    SET_CHATTERER(state, value) { state.chatterer = value; },
    SET_ONLINE(state, value) { state.online = value; },
    SET_TAKE_PROFIT(state, value) { state.take_profit = value; },
    SET_SYMBOLS(state, value) { state.symbols = value; },
    SET_SYMBOLS_SETS(state, value) { state.symbols_sets = value; },
    SET_CUR1(state, value) { state.cur1 = value; },
    SET_CUR2(state, value) { state.cur2 = value; },
    SET_DRAWER(state, value) { state.drawer = value; },
    SET_PANIK(state, value) { state.panik = value; },
  },
  actions: {
    get_chatterer({ commit }) {
      axios.get(`/api/v1/ui/knightrider`).then(response => {
        commit('SET_CHATTERER', response.data.chatterer);
      })
    },
    get_online({commit}) {
      axios.get(`/api/v1/ui/online`).then(response => {
        commit('SET_ONLINE', response.data.online);
      })
    },
    get_currencies({commit}) {
      axios.get(`/api/v1/ui/currency`).then(response => {
        commit('SET_CUR1', response.data.cur1);
        commit('SET_CUR2', response.data.cur2);
      })
    },
    get_symbols({commit}) {
      axios.get(`/api/v1/ui/symbols`).then(response => {
        commit('SET_SYMBOLS', response.data.symbols);
      })
      axios.get(`/api/v1/ui/symbols_sets`).then(response => {
        commit('SET_SYMBOLS_SETS', response.data.symbols);
      })
    },
    get_take_profit({commit}) {
      axios.get(`/api/v1/configure/take_profit`).then(response => {
        commit('SET_TAKE_PROFIT', response.data.take_profit);
      })
    },
    set_take_profit(state, value) {
      if(value != state.take_profit) {
        axios.post(`/api/v1/configure/take_profit`, {'tp': value});
      }
    },
    toggle_online() {
      axios.get(`/api/v1/configure/online`);
    },
    set_cur1({commit}, value) {
      axios.post(`/api/v1/configure/cur1`, {'cur': value}).then(response => {
        commit('SET_CUR1', response.data.cur1);
        commit('SET_CUR2', response.data.cur2);
      });
    },
    set_cur2({commit}, value) {
      axios.post(`/api/v1/configure/cur2`, {'cur': value}).then(response => {
        commit('SET_CUR1', response.data.cur1);
        commit('SET_CUR2', response.data.cur2);
      });
    },
    toggle_drawer(state, v) {
      state.commit('SET_DRAWER', v);
    },
    set_panik({commit}, value) {
      axios.post(`/api/v1/configure/panik`, {'panik': value}).then(response => {
        commit('SET_PANIK', response.data.panik);
      });
    },
  },
  modules: {
  }
})
