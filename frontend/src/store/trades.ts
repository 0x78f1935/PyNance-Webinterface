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
        profitAs: '',
        spot: true,
        sandbox: true
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
        spot: state => state.spot,
        sandbox: state => state.sandbox,
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
        SET_PROFIT_MARGIN(state, value) { state.profitMargin = value; },
        SET_PROFIT_AS(state, value) { state.profitAs = value; },
        SET_SPOT(state, value) { state.spot = value; },
        SET_SANDBOX(state, value) { state.sandbox = value; },
    },

    actions: {
        loadTrades(state) {
            axios.get(`/api/v1/trades/`, {headers: {'token': localStorage['sk']}}).then(response => {
                state.commit('SET_SANDBOX', response.data.sandbox);
                state.commit('SET_ASSETS', response.data.assets);
                state.commit('SET_SYMBOLS', response.data.symbols);
                state.commit('SET_SYMBOLS_CHOICES', response.data["symbols-choices"]);                
                state.commit('SET_TIMEFRAME_CHOICES', response.data["timeframe-choices"]);
                state.commit('SET_TIMEFRAME', response.data["timeframe"]);
                state.commit('SET_CANDLE_INTERVAL', response.data["candle-interval"]);
                state.commit('SET_WALLET_AMOUNT', response.data["wallet-amount"]);
                state.commit('SET_BELOW_AVERAGE', response.data["below-average"]);
                state.commit('SET_PROFIT_MARGIN', response.data["profit-margin"]);
                state.commit('SET_PROFIT_AS', response.data["profit-as"]);
                state.commit('SET_SPOT', response.data["spot"]);
                state.commit('SET_EXPECTED_LEVERAGE', response.data["expected-leverage"]);
                state.commit('SET_ACTIVATE_PRICE', response.data["activation-price"]);
                state.commit('SET_IN_GREEN', response.data["in-green"]);
                state.commit('SET_USE_AVERAGE', response.data["use-average"]);
                state.commit('SET_VOLUME_TIME_FRAME', response.data["volume-timeframe"]);
                state.commit('SET_TOTAL_VOLUME', response.data["total-volume"]);
                state.commit('SET_MARGIN_TYPE', response.data["margin-type"]);
                console.log(response.data);
            });
        },
        saveTradeConfig(state) {
            axios.post(`/api/v1/trades/`, {
                sandbox: state.getters.sandbox,
                symbols: state.getters.symbols,
                timeframe: state.getters.timeframe,
                candle_interval: state.getters.candleInterval,
                wallet_amount: state.getters.walletAmount,
                below_average: state.getters.belowAverage,
                profit_margin: state.getters.profitMargin,
                profit_as: state.getters.profitAs,
                spot: state.getters.spot,
                activation_price: state.getters.activatePrice,
                in_green: state.getters.inGreen,
                use_average: state.getters.useAverage,
                expected_leverage: state.getters.expectedLeverage,
                volume_timeframe: state.getters.volumeTimeFrame,
                total_volume: state.getters.totalVolume,
                margin_type: state.getters.marginType,
            },{headers: {'token': state.getters.token}});
        }
    }
}

export default tradesModule;
