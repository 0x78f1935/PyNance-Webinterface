import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import Config from '../views/Config.vue';
import Authenticate from '../views/Authenticate.vue';
import Statistics from '../views/Statistics.vue';
import Trades from '../views/Trades.vue';
import Wallet from '../views/Wallet.vue';
import Guide from '../views/Guide.vue';
import News from '../views/News.vue';

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/config',
    name: 'Config',
    component: Config
  },
  {
    path: '/news',
    name: 'News',
    component: News
  },
  {
    path: '/',
    name: 'Authenticate',
    component: Authenticate
  },
  {
    path: '/statistics',
    name: 'Statistics',
    component: Statistics
  },
  {
    path: '/trades',
    name: 'Trades',
    component: Trades
  },
  {
    path: '/wallet',
    name: 'Wallet',
    component: Wallet
  },
  {
    path: '/guide',
    name: 'Guide',
    component: Guide
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
