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
  },
  getters: {
    darkmode: state => { return state.darkmode; },
    chatterer: state => { return state.chatterer; },
    online: state => { return state.online; },
    take_profit: state => { return state.take_profit; }
  },
  mutations: {
    SET_DARKMODE(state, value) { state.darkmode = value; },
    SET_CHATTERER(state, value) { state.chatterer = value; },
    SET_ONLINE(state, value) { state.online = value },
    SET_TAKE_PROFIT(state, value) { state.take_profit = value },
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
    toggle_online(state) {
      axios.get(`/api/v1/configure/online`);
    }
  },
  modules: {
  }
})
