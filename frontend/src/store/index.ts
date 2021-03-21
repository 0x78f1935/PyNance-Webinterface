import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios';

Vue.use(Vuex)


export default new Vuex.Store({
  state: {
    languages: ['en', 'fil', 'fr', 'nl'],
    timeframes: ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'],
    symbols: [],
    drawer: true,
    disclaimer: true,
    tos: false,
    symbol: "",
    profit: 0,
    profitColor: 'accent',
    twitter: 'https://twitter.com/UnicodeError',
    github: 'https://github.com/0x78f1935/PyNance-Webinterface',

    // System
    currency1: "",
    currency2: "",
    online: false,

    // Preferences
    language: 'en',
    darkmode: true,
    panik: false,
    version: 'x.x.x',
    authentication: false,
    authenticated: true,
    token: '',
    
    // Settings
    valid: false,
    minimalProfit: 20.0,
    walletAmount: 99,
    timeframe: '1m',
    candles: 100,
    averageDistance: 0,
    selectedProfit: 'USDT',

    // Bot
    msg: 'Starting up ...',
    currentPrice: 0,
    averagePrice: 0,
    orders: {'headers': [], 'data': []},
  },
  getters:{
    drawer: state => { return state.drawer; },
    disclaimer: state => { return state.disclaimer; },
    tos: state => { return state.tos; },
    symbols: state => { return state.symbols; },
    timeframes: state => { return state.timeframes; },
    languages: state => { return state.languages; },
    symbol: state => { return state.symbol; },
    profit: state => { return state.profit; },
    profitColor: state => { return state.profitColor; },
    twitter: state => { return state.twitter; },
    github: state => { return state.github; },
    
    // System
    currency1: state => { return state.currency1; },
    currency2: state => { return state.currency2; },
    online: state => { return state.online; },

    // Preferences
    language: state => { return state.language; },
    darkmode: state => { return state.darkmode; },
    panik: state => { return state.panik; },
    version: state => { return state.version; },
    authentication: state => { return state.authentication; },
    authenticated: state => { return state.authenticated; },
    token: state => { return state.token; },

    // Settings
    valid: state => { return state.valid; },
    minimalProfit: state => { return state.minimalProfit; },
    walletAmount: state => { return state.walletAmount; },
    timeframe: state => { return state.timeframe; },
    candles: state => { return state.candles; },
    averageDistance: state => { return state.averageDistance; },
    selectedProfit: state => { return state.selectedProfit; },    

    // Bot
    msg: state => { return state.msg; },
    currentPrice: state => { return state.currentPrice},
    averagePrice: state => { return state.averagePrice},

    orders: state => { return state.orders; },
  },
  mutations: {
    SET_DRAWER(state, value) { state.drawer = value; },
    SET_DISCLAIMER(state, value) { state.disclaimer = value; },
    SET_TOS(state, value) { state.tos = value; },
    SET_SYMBOLS(state, value) { state.symbols = value; },
    SET_SYMBOL(state, value) { state.symbol = value; },
    SET_PROFIT(state, value) { state.profit = value; },
    SET_PROFIT_COLOR(state, value) { state.profitColor = value; },
    
    // System
    SET_CURRENCY_1(state, value) { state.currency1 = value; },
    SET_CURRENCY_2(state, value) { state.currency2 = value; },
    SET_ONLINE(state, value) { state.online = value; },

    // Preferences
    SET_DARKMODE(state, value) { state.darkmode = value; },
    SET_VERSION(state, value) { state.version = value; },
    SET_LANGUAGE(state, value) { state.language = value; },
    SET_PANIK(state, value) { state.panik = value; },
    SET_AUTHENTICATION(state, value) { state.authentication = value; },
    SET_AUTHENTICATED(state, value) { state.authenticated = value; },
    SET_TOKEN(state, value) { state.token = value; },

    // Settings
    SET_VALID(state, value) { state.valid = value; },
    SET_MINIMAL_PROFIT(state, value) { state.minimalProfit = value; },
    SET_WALLET_AMOUNT(state, value) { state.walletAmount = value; },
    SET_TIMEFRAME(state, value) { state.timeframe = value; },
    SET_CANDLES(state, value) { state.candles = value; },
    SET_AVERAGE_DISTANCE(state, value) { state.averageDistance = value; },
    SET_SELECTED_PROFIT(state, value) { state.selectedProfit = value; },
    
    // Bots
    SET_MSG(state, value) { state.msg = value; },
    SET_CURRENT_PRICE(state, value) {state.currentPrice = value; },
    SET_AVERAGE_PRICE(state, value) {state.averagePrice = value; },

    SET_ORDERS(state, value) { state.orders = value; },
  },
  actions: {

    setDisclaimer(state, value) {
      state.commit('SET_DISCLAIMER', value);
    },
    // System
    toggleDrawer(state, value) {
      state.commit('SET_DRAWER', value);
    },

    initApp(state) {
      axios.get(`/api/v1/preference/`, {headers: {'token': localStorage['sk']}}).then(response => {
        state.commit('SET_LANGUAGE', response.data.language);
        state.commit('SET_PANIK', response.data.panik);
        state.commit('SET_VERSION', response.data.version);
        state.commit('SET_AUTHENTICATION', response.data.authentication);
        state.commit('SET_TOKEN', response.data.token);
        if(state.getters.authentication) {
          state.commit('SET_AUTHENTICATED', false);
        }
      });

      axios.get(`/api/v1/system/all`, {headers: {'token': localStorage['sk']}}).then(response => {
        state.commit('SET_CURRENCY_1', response.data.currency_1);
        state.commit('SET_CURRENCY_2', response.data.currency_2);
        state.commit('SET_SYMBOLS', response.data.symbols);
        state.commit('SET_SYMBOL', response.data.symbol);
        state.commit('SET_ONLINE', response.data.online);
        state.commit('SET_TOS', response.data.tos_agreement);
        if(state.getters.tos) {
          state.commit('SET_DISCLAIMER', false);
        }
      });

      axios.get(`/api/v1/settings/`, {headers: {'token': localStorage['sk']}}).then(response => {
        state.commit('SET_VALID', response.data.valid);
        state.commit('SET_MINIMAL_PROFIT', response.data.minimal_profit);
        state.commit('SET_WALLET_AMOUNT', response.data.wallet_amount);
        state.commit('SET_TIMEFRAME', response.data.timeframe);
        state.commit('SET_CANDLES', response.data.total_candles);
        state.commit('SET_AVERAGE_DISTANCE', response.data.average_distance);
        state.commit('SET_SELECTED_PROFIT', response.data.selected_profit);
      });

      axios.get(`/api/v1/bot/msg`, {headers: {'token': localStorage['sk']}}).then(response => {
        state.commit('SET_MSG', response.data.information);
        state.commit('SET_CURRENT_PRICE', response.data.current_value);
        state.commit('SET_AVERAGE_PRICE', response.data.average_price);
      });

      axios.post(`/api/v1/system/profit`, {'symbol': state.getters.selectedProfit}, {headers: {'token': localStorage['sk']}}).then(response => {
        state.commit('SET_PROFIT', response.data.profit);
        state.commit('SET_PROFIT_COLOR', response.data.color);
      });

    },

    getProfit(state) {
      axios.post(`/api/v1/system/profit`, {'symbol': state.getters.selectedProfit}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_PROFIT', response.data.profit);
        state.commit('SET_PROFIT_COLOR', response.data.color);
      });
    },

    // Settings
    setCurrency1(state, value) {
      axios.post(`/api/v1/system/`, {'currency_1': value}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_CURRENCY_1', response.data.currency_1);
      });
    },
    setCurrency2(state, value) {
      axios.post(`/api/v1/system/`, {'currency_2': value}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_CURRENCY_2', response.data.currency_2);
      });
    },
    setOnline(state, value) {
      axios.post(`/api/v1/system/`, {'online': value}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_ONLINE', response.data.online);
      });
    },
    getOnline(state) {
      axios.get(`/api/v1/system/`, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_ONLINE', response.data.online);
      });
    },
    setTos(state, value) {
      axios.post(`/api/v1/system/`, {'tos_agreement': value}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_TOS', response.data.tos_agreement);
      });
    },
    setMinimalProfit(state, value){
      if (/^[0-9\-]*$/.test(value)){
        if(value > 0) {
          axios.post(`/api/v1/settings/`, {'minimal_profit': value}, {headers: {'token': state.getters.token}}).then(response => {
            state.commit('SET_MINIMAL_PROFIT', response.data.minimal_profit);
          });
        }
      }
    },
    setWalletAmount(state, value){
      if (/^[0-9\-]*$/.test(value)){
        if(value > 0 && value <= 100) {
            axios.post(`/api/v1/settings/`, {'wallet_amount': value}, {headers: {'token': state.getters.token}}).then(response => {
              state.commit('SET_WALLET_AMOUNT', response.data.wallet_amount);
            });
        }
      }
    },
    setTimeframe(state, value){
      axios.post(`/api/v1/settings/`, {'timeframe': value}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_TIMEFRAME', response.data.timeframe);
      });
    },
    setCandles(state, value){
      axios.post(`/api/v1/settings/`, {'total_candles': value}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_CANDLES', response.data.total_candles);
      });
    },
    setAverageDistance(state, value){
      if (/^[+-]?\d+(\.\d+)?$/.test(value)){
        if(value >= 0 && value <= 100) {
          axios.post(`/api/v1/settings/`, {'average_distance': value}, {headers: {'token': state.getters.token}}).then(response => {
            state.commit('SET_AVERAGE_DISTANCE', response.data.average_distance);
          });
        }
      }
    },
    setSelectedProfit(state, value){
      axios.post(`/api/v1/settings/`, {'selected_profit': value}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_SELECTED_PROFIT', response.data.selected_profit);
      });
    },

    // Preferences
    setLanguage(state, value){
      axios.post(`/api/v1/preference/`, {'language': value}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_LANGUAGE', response.data.language);
      });
    },

    setPanik(state, value){
      axios.post(`/api/v1/preference/`, {'panik': value}, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_PANIK', response.data.panik);
      });
    },

    // Bot
    getMsg(state){
      axios.get(`/api/v1/bot/msg`, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_MSG', response.data.information);
        state.commit('SET_CURRENT_PRICE', response.data.current_value);
        state.commit('SET_AVERAGE_PRICE', response.data.average_price);
      });
    },

    getPrice(state){
      axios.get(`/api/v1/bot/current_price?cur1=${state.getters.currency1}&cur2=${state.getters.currency2}`, {headers: {'token': state.getters.token}}).then(response => {
        state.commit('SET_CURRENT_PRICE', response.data.current_value);
        state.commit('SET_AVERAGE_PRICE', response.data.average_price);
      });
    },

    getOrders( state ) {
      axios.get(`/api/v1/orders/`, {headers: {'token': state.getters.token}}).then(resp => {
        if(resp.data.length > 0) {
            let headers = Object.keys(resp.data[0]).map(item => { 
                let value = '';
                if (item == 'quantity') { value = 'Quantity';}
                else if (item == 'brought') { value = 'Brought';}
                else if (item == 'updated') { value = 'Updated';}
                else if (item == 'symbol') { value = 'Symbol';}
                else if (item == 'brought_price') { value = 'Brought Price';}
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
            state.commit('SET_ORDERS', {'headers': headers, 'data': items})
        } else {
          state.commit('SET_ORDERS', {'headers': [], 'data': []})
        }
      });
    },

    getBackup(state){
      axios.get(`/api/v1/backup`, {responseType: 'blob', headers: {'token': state.getters.token}}).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        const fileName = `backup_${+ new Date()}.pynance`// whatever your file name .
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        link.remove();// you need to remove that elelment which is created before.
      });
    },

    restoreBackup(state, data ) {
      const formdata = new FormData();
      formdata.append('backup', data.backup);
      axios.post(`/api/v1/backup/`, formdata, {
        headers: {
          'Content-Type': 'text/plain',
          'token': state.getters.token
        }
      }).then((response) => {
        if(response.data.succes) {
          data.callbackNotifier(data.done, 5000);
        } else {
          data.callbackNotifier(data.try, 5000);
        }
      });
    }

  },
  modules: {
  }
})
