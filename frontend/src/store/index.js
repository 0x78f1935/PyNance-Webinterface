import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
axios.defaults.baseURL = process.env.SERVER_BACKEND;

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    darkmode: true,
    chatterer: "",
    online: false,
    take_profit: 0,
    total_entry: 100,
    symbols: [],
    symbols_sets: [],
    cur1: "",
    cur2: "",
    drawer: true,
    panik: false,
    only_dip: true,
    version: "",
    maintainer: "",
    github: "",
    twitter: "",
    profit: "",
    orders: {'headers': [], 'data': []},
    languages: ['en', 'nl', 'fr', 'fil'],
    language: "en",
    fiat_current_price: "0",
    coin_current_price: "0",
    current_quantity: "0",
    current_price: "",
  },
  getters: {
    darkmode: state => { return state.darkmode; },
    chatterer: state => { return state.chatterer; },
    online: state => { return state.online; },
    take_profit: state => { return state.take_profit; },
    total_entry: state => { return state.total_entry; },
    symbols: state => { return state.symbols; },
    symbols_sets: state => { return state.symbols_sets; },
    cur1: state => { return state.cur1; },
    cur2: state => { return state.cur2; },
    drawer: state => { return state.drawer; },
    panik: state => { return state.panik; },
    only_dip: state => { return state.only_dip; },
    version: state => { return state.version; },
    maintainer: state => { return state.maintainer; },
    github: state => { return state.github; },
    twitter: state => { return state.twitter; },
    profit: state => { return state.profit; },
    orders: state => { return state.orders; },
    languages: state => { return state.languages; },
    language: state => { return state.language; },
    fiat_current_price: state => { return state.fiat_current_price; },
    coin_current_price: state => { return state.coin_current_price; },
    current_quantity: state => { return state.current_quantity; },
    current_price: state => { return state.current_price; }
  },
  mutations: {
    SET_DARKMODE(state, value) { state.darkmode = value; },
    SET_CHATTERER(state, value) { state.chatterer = value; },
    SET_ONLINE(state, value) { state.online = value; },
    SET_TAKE_PROFIT(state, value) { state.take_profit = value; },
    SET_TOTAL_ENTRY(state, value) { state.total_entry = value; },
    SET_SYMBOLS(state, value) { state.symbols = value; },
    SET_SYMBOLS_SETS(state, value) { state.symbols_sets = value; },
    SET_CUR1(state, value) { state.cur1 = value; },
    SET_CUR2(state, value) { state.cur2 = value; },
    SET_DRAWER(state, value) { state.drawer = value; },
    SET_PANIK(state, value) { state.panik = value; },
    SET_ONLY_DIP(state, value) { state.only_dip = value; },
    SET_VERSION(state, value) { state.version = value; },
    SET_MAINTAINER(state, value) { state.maintainer = value; },
    SET_GITHUB(state, value) { state.github = value; },
    SET_TWITTER(state, value) { state.twitter = value; },
    SET_PROFIT(state, value) { state.profit = value; },
    SET_ORDERS(state, value) { state.orders = value; },
    SET_LANGUAGE(state, value) { state.language = value; },
    SET_CURRENT_FIAT(state, value) { state.fiat_current_price = value; },
    SET_CURRENT_COINT(state, value) { state.coin_current_price = value; },
    SET_CURRENT_QUANTITY(state, value) { state.current_quantity = value; },
    SET_CURRENT_PRICE(state, value) {state.current_price = value; }
  },
  actions: {
    get_chatterer(state) {
      axios.get(`/api/v1/ui/knightrider`).then(response => {
        state.commit('SET_CHATTERER', response.data.chatterer);
      })
    },
    get_version(state) {
      axios.get(`/api/v1/ui/version`).then(response => {
        state.commit('SET_VERSION', response.data.version);
      })
    },
    get_current_coin_price(state) {
      axios.get(`/api/v1/ui/current_price`).then(response => {
        state.commit('SET_CURRENT_FIAT', response.data.fiat);
        state.commit('SET_CURRENT_COINT', response.data.coin);
        state.commit('SET_CURRENT_QUANTITY', response.data.quantity);
      })
    },
    get_current_price(state) {
      axios.get(`/api/v1/ui/v2/current_price`).then(response => {
        state.commit('SET_CURRENT_PRICE', response.data.price);
      })
    },
    get_profit(state) {
      axios.get(`/api/v1/ui/profit`).then(response => {
        state.commit('SET_PROFIT', response.data.profit);
      })
    },
    get_maintainer(state) {
      axios.get(`/api/v1/ui/maintainer`).then(response => {
        state.commit('SET_MAINTAINER', response.data.maintainer);
        state.commit('SET_GITHUB', response.data.github);
        state.commit('SET_TWITTER', response.data.twitter);
      })
    },
    get_online(state) {
      axios.get(`/api/v1/ui/online`).then(response => {
        state.commit('SET_ONLINE', response.data.online);
      })
    },
    get_currencies(state) {
      axios.get(`/api/v1/ui/currency`).then(response => {
        state.commit('SET_CUR1', response.data.cur1);
        state.commit('SET_CUR2', response.data.cur2);
      })
    },
    get_symbols(state) {
      axios.get(`/api/v1/ui/symbols`).then(response => {
        state.commit('SET_SYMBOLS', response.data.symbols);
      })
      if(state.getters.cur1.length > 0 && state.getters.cur2 > 0) {
        axios.get(`/api/v1/ui/symbols_sets?symbol=${state.getters.cur1}${state.getters.cur1}`).then(response => {
          state.commit('SET_SYMBOLS_SETS', response.data.symbols);
        })
      }
    },
    get_take_profit(state) {
      axios.get(`/api/v1/configure/take_profit`).then(response => {
        state.commit('SET_TAKE_PROFIT', response.data.take_profit);
      })
    },
    set_take_profit(state, value) {
      if(value != state.take_profit) {
        axios.post(`/api/v1/configure/take_profit`, {'tp': value});
      }
    },
    get_total_entry(state) {
      axios.get(`/api/v1/configure/total_entry`).then(response => {
        state.commit('SET_TOTAL_ENTRY', response.data.total_entry);
      })
    },
    set_total_entry(state, value) {
      if(value != state.total_entry) {
        axios.post(`/api/v1/configure/total_entry`, {'total_entry': value});
      }
    },
    toggle_online() {
      axios.get(`/api/v1/configure/online`);
    },
    set_cur1(state, value) {
      axios.post(`/api/v1/configure/cur1`, {'cur': value}).then(response => {
        state.commit('SET_CUR1', response.data.cur1);
        state.commit('SET_CUR2', response.data.cur2);
      });
    },
    set_cur2(state, value) {
      axios.post(`/api/v1/configure/cur2`, {'cur': value}).then(response => {
        state.commit('SET_CUR1', response.data.cur1);
        state.commit('SET_CUR2', response.data.cur2);
      });
    },
    toggle_drawer(state, v) {
      state.commit('SET_DRAWER', v);
    },
    set_panik(state, value) {
      axios.post(`/api/v1/configure/panik`, {'panik': value}).then(response => {
        state.commit('SET_PANIK', response.data.panik);
      });
    },
    get_panik(state) {
      axios.get(`/api/v1/configure/panik`).then(response => {
        state.commit('SET_PANIK', response.data.panik);
      });
    },
    get_only_dip(state) {
      axios.get(`/api/v1/configure/only_dip`).then(response => {
        state.commit('SET_ONLY_DIP', response.data.dip);
      });
    },
    set_only_dip(state, value) {
      axios.post(`/api/v1/configure/only_dip`, {'dip': !value}).then(response => {
        state.commit('SET_ONLY_DIP', response.data.dip);
      });
    },
    get_orders( { commit }) {
      axios.get(`/api/v1/orders/`).then(resp => {
        if(resp.data.length > 0) {
            let headers = Object.keys(resp.data[0]).map(item => { 
                let value = '';
                if (item == 'quantity') { value = 'Quantity';}
                else if (item == 'paid_total') { value = 'Paid including fees';}
                else if (item == 'total_fee_paid') { value = 'Fee costs';}
                else if (item == 'total_paid_minus_fee') { value = 'Paid excluding fee';}
                else if (item == 'wanted_profit') { value = 'Expected profit';}
                else if (item == 'sellprice_without_loss_on_fee_plus_profit') { value = 'Sell target';}
                else if (item == 'sold_for') { value = 'Sold for';}
                else { value = item;}
                return {
                    text: value,
                    value: item,
                    sortable: true,
                    filterable: true
                } 
            });
            let items = resp.data;
            commit('SET_ORDERS', {'headers': headers, 'data': items})
        }
    });
    }
  },
  modules: {
  }
})
