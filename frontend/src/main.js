import '@babel/polyfill';
import 'mutationobserver-shim';
import Vue from 'vue';
import './plugins/bootstrap-vue';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import './plugins/apexcharts.js';
import i18n from './i18n';

Vue.config.productionTip = false;

new Vue(
  {
    router,
    store,
    vuetify,
    i18n,
    render: h => h(App)
  }
).$mount('#app')
