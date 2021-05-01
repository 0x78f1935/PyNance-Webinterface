import { Module } from "vuex";
import axios from 'axios';

const tradesModule: Module<any, any> = { 
    state: {
        assets: [],
        symbols: [],
        symbolsChoices: [],
        timeframeChoices: [],
        timeframe: '',
        candleInterval: 0,
        walletAmount: 0,
        belowAverage: 0,
        profitMargin: 0,
        profitAs: ''
    },

    getters: {
        assets: state => state.assets,
        symbols: state => state.symbols,
        symbolsChoices: state => state.symbolsChoices,
        timeframeChoices: state => state.timeframeChoices,
        timeframe: state => state.timeframe,
        candleInterval: state => state.candleInterval,
        walletAmount: state => state.walletAmount,
        belowAverage: state => state.belowAverage,
        profitMargin: state => state.profitMargin,
        profitAs: state => state.profitAs,
    },

    mutations: {
        SET_ASSETS(state, value) { state.assets = value; },
        SET_SYMBOLS(state, value) { state.symbols = value; },
        SET_SYMBOLS_CHOICES(state, value) { state.symbolsChoices = value; },
        SET_TIMEFRAME_CHOICES(state, value) { state.timeframeChoices = value; },
        SET_TIMEFRAME(state, value) { state.timeframe = value; },
        SET_CANDLE_INTERVAL(state, value) { state.candleInterval = value; },
        SET_WALLET_AMOUNT(state, value) { state.walletAmount = value; },
        SET_BELOW_AVERAGE(state, value) { state.belowAverage = value; },
        SET_BELOW_PROFIT_MARGIN(state, value) { state.profitMargin = value; },
        SET_PROFIT_AS(state, value) { state.profitAs = value; },
    },

    actions: {
        loadTrades(state) {
            axios.get(`/api/v1/trades/`, {headers: {'token': localStorage['sk']}}).then(response => {
                state.commit('SET_ASSETS', response.data.assets);
                state.commit('SET_SYMBOLS', response.data.symbols);
                state.commit('SET_SYMBOLS_CHOICES', response.data["symbols-choices"]);                
                state.commit('SET_TIMEFRAME_CHOICES', response.data["timeframe-choices"]);
                state.commit('SET_TIMEFRAME', response.data["timeframe"]);
                state.commit('SET_CANDLE_INTERVAL', response.data["candle-interval"]);
                state.commit('SET_WALLET_AMOUNT', response.data["wallet-amount"]);
                state.commit('SET_BELOW_AVERAGE', response.data["below-average"]);
                state.commit('SET_BELOW_PROFIT_MARGIN', response.data["profit-margin"]);
                state.commit('SET_PROFIT_AS', response.data["profit-as"]);
                console.log(response.data);
            });
        }
    }
}

export default tradesModule;
