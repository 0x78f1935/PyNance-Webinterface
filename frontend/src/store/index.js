import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    darkmode: true,
    chatterer: "",
  },
  getters: {
    darkmode: state => { return state.darkmode; },
    chatterer: state => { return state.chatterer; }
  },
  mutations: {
    SET_DARKMODE(state, value) { state.darkmode = value; },
    SET_CHATTERER(state, value) { state.chatterer = value; } 
  },
  actions: {
    get_chatterer({ commit }) {
      axios.get(`/api/v1/ui/knightrider`).then(response => {
        commit('SET_CHATTERER', response.data.chatterer);
      })
    },
  },
  modules: {
  }
})
