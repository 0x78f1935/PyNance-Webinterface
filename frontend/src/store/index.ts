import Vue from 'vue';
import Vuex from 'vuex';

import bot from './bot';
import keys from './keys';
import system from './system';
import trades from './trades';
import backup from './backup';
import futures from './futures';

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    bot,
    keys,
    system,
    trades,
    backup,
    futures
  },
})
