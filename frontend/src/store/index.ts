import Vue from 'vue';
import Vuex from 'vuex';

import bot from './bot';
import keys from './keys';
import system from './system';

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    bot,
    keys,
    system
  },
})
