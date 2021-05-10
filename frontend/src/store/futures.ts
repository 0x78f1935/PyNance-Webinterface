import { Module } from "vuex";
import axios from 'axios';

const futuresModule: Module<any, any> = { 
    state: {
        expectedLeverage: 0,
        activatePrice: 0,
        inGreen: 0,
        useAverage: false,
        volumeTimeFrame: "",
        volumeTimeFrameSelection: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"],
        totalVolume: 0,
        marginType: '',
        marginTypeChoices: ['ISOLATED', 'CROSSED'],
        allowMultipleOrders: false,
    },

    getters: {
        expectedLeverage: state => state.expectedLeverage,
        activatePrice: state => state.activatePrice,
        inGreen: state => state.inGreen,
        useAverage: state => state.useAverage,
        volumeTimeFrame: state => state.volumeTimeFrame,
        volumeTimeFrameSelection: state => state.volumeTimeFrameSelection,
        totalVolume: state => state.totalVolume,
        marginType: state => state.marginType,
        marginTypeChoices: state => state.marginTypeChoices,
        allowMultipleOrders: state => state.allowMultipleOrders,
    },

    mutations: {
        SET_EXPECTED_LEVERAGE(state, value) { state.expectedLeverage = value; },
        SET_ACTIVATE_PRICE(state, value) { state.activatePrice = value; },
        SET_IN_GREEN(state, value) { state.inGreen = value; },
        SET_USE_AVERAGE(state, value) { state.useAverage = value; },
        SET_VOLUME_TIME_FRAME(state, value) { state.volumeTimeFrame = value; },
        SET_TOTAL_VOLUME(state, value) { state.totalVolume = value; },
        SET_MARGIN_TYPE(state, value) { state.marginType = value; },
        SET_ALLOW_MULTIPLE_ORDERS(state, value) { state.allowMultipleOrders = value; },
    },

    actions: {

    }
}

export default futuresModule;
