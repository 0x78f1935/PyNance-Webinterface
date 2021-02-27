import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    darkmode: true,
    chatterer: "",
    online: false,
  },
  getters: {
    darkmode: state => { return state.darkmode; },
    chatterer: state => { return state.chatterer; },
    online: state => { return state.online; }
  },
  mutations: {
    SET_DARKMODE(state, value) { state.darkmode = value; },
    SET_CHATTERER(state, value) { state.chatterer = value; },
    SET_ONLINE(state, value) { state.online = value },
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
    }
  },
  modules: {
  }
})
