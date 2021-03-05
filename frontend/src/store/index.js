import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    endpoint: "http://127.0.0.1:5000",
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
    version: "",
    maintainer: "",
    github: "",
    twitter: "",
    profit: "",
  },
  getters: {
    endpoint: state => { return state.endpoint; },
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
    version: state => { return state.version; },
    maintainer: state => { return state.maintainer; },
    github: state => { return state.github; },
    twitter: state => { return state.twitter; },
    profit: state => { return state.profit; },
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
    SET_VERSION(state, value) { state.version = value; },
    SET_MAINTAINER(state, value) { state.maintainer = value; },
    SET_GITHUB(state, value) { state.github = value; },
    SET_TWITTER(state, value) { state.twitter = value; },
    SET_PROFIT(state, value) { state.profit = value; },
  },
  actions: {
    get_chatterer({ commit, getters }) {
      axios.get(`${getters.endpoint}/api/v1/ui/knightrider`).then(response => {
        commit('SET_CHATTERER', response.data.chatterer);
      })
    },
    get_version({ commit, getters }) {
      axios.get(`${getters.endpoint}/api/v1/ui/version`).then(response => {
        commit('SET_VERSION', response.data.version);
      })
    },
    get_profit({ commit, getters }) {
      axios.get(`${getters.endpoint}/api/v1/ui/profit`).then(response => {
        commit('SET_PROFIT', response.data.profit);
      })
    },
    get_maintainer({ commit, getters }) {
      axios.get(`${getters.endpoint}/api/v1/ui/maintainer`).then(response => {
        commit('SET_MAINTAINER', response.data.maintainer);
        commit('SET_GITHUB', response.data.github);
        commit('SET_TWITTER', response.data.twitter);
      })
    },
    get_online({commit, getters}) {
      axios.get(`${getters.endpoint}/api/v1/ui/online`).then(response => {
        commit('SET_ONLINE', response.data.online);
      })
    },
    get_currencies({commit, getters}) {
      axios.get(`${getters.endpoint}/api/v1/ui/currency`).then(response => {
        commit('SET_CUR1', response.data.cur1);
        commit('SET_CUR2', response.data.cur2);
      })
    },
    get_symbols({commit, getters}) {
      axios.get(`${getters.endpoint}/api/v1/ui/symbols`).then(response => {
        commit('SET_SYMBOLS', response.data.symbols);
      })
      axios.get(`${getters.endpoint}/api/v1/ui/symbols_sets`).then(response => {
        commit('SET_SYMBOLS_SETS', response.data.symbols);
      })
    },
    get_take_profit({commit, getters}) {
      axios.get(`${getters.endpoint}/api/v1/configure/take_profit`).then(response => {
        commit('SET_TAKE_PROFIT', response.data.take_profit);
      })
    },
    set_take_profit(state, value) {
      if(value != state.take_profit) {
        axios.post(`${getters.endpoint}/api/v1/configure/take_profit`, {'tp': value});
      }
    },
    toggle_online() {
      axios.get(`${getters.endpoint}/api/v1/configure/online`);
    },
    set_cur1({commit, getters}, value) {
      axios.post(`${getters.endpoint}/api/v1/configure/cur1`, {'cur': value}).then(response => {
        commit('SET_CUR1', response.data.cur1);
        commit('SET_CUR2', response.data.cur2);
      });
    },
    set_cur2({commit, getters}, value) {
      axios.post(`${getters.endpoint}/api/v1/configure/cur2`, {'cur': value}).then(response => {
        commit('SET_CUR1', response.data.cur1);
        commit('SET_CUR2', response.data.cur2);
      });
    },
    toggle_drawer(state, v) {
      state.commit('SET_DRAWER', v);
    },
    set_panik({commit, getters}, value) {
      axios.post(`${getters.endpoint}/api/v1/configure/panik`, {'panik': value}).then(response => {
        commit('SET_PANIK', response.data.panik);
      });
    },
  },
  modules: {
  }
})
