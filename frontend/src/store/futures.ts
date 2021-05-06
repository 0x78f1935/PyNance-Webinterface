import { Module } from "vuex";
import axios from 'axios';

const futuresModule: Module<any, any> = { 
    state: {
        expectedLeverage: 0,
        defaultStopLoss: 0,
        totalTP: 0,
        inGreen: 0,
        moveStopLoss: 0,
        takeProfit: 0,
        useAverage: false,
        volumeTimeFrame: "",
        volumeTimeFrameSelection: ["5m","15m","30m","1h","2h","4h","6h","12h","1d"],
        totalVolume: 0,
        marginType: '',
        marginTypeChoices: ['ISOLATED', 'CROSSED']
    },

    getters: {
        expectedLeverage: state => state.expectedLeverage,
        defaultStopLoss: state => state.defaultStopLoss,
        totalTP: state => state.totalTP,
        inGreen: state => state.inGreen,
        moveStopLoss: state => state.moveStopLoss,
        takeProfit: state => state.takeProfit,
        useAverage: state => state.useAverage,
        volumeTimeFrame: state => state.volumeTimeFrame,
        volumeTimeFrameSelection: state => state.volumeTimeFrameSelection,
        totalVolume: state => state.totalVolume,
        marginType: state => state.marginType,
        marginTypeChoices: state => state.marginTypeChoices,
    },

    mutations: {
        SET_EXPECTED_LEVERAGE(state, value) { state.expectedLeverage = value; },
        SET_DEFAULT_STOP_LOSS(state, value) { state.defaultStopLoss = value; },
        SET_TOTAL_TP(state, value) { state.totalTP = value; },
        SET_IN_GREEN(state, value) { state.inGreen = value; },
        SET_MOVE_STOP_LOSS(state, value) { state.moveStopLoss = value; },
        SET_TAKE_PROFIT(state, value) { state.takeProfit = value; },
        SET_USE_AVERAGE(state, value) { state.useAverage = value; },
        SET_VOLUME_TIME_FRAME(state, value) { state.volumeTimeFrame = value; },
        SET_TOTAL_VOLUME(state, value) { state.totalVolume = value; },
        SET_MARGIN_TYPE(state, value) { state.marginType = value; },
    },

    actions: {

    }
}

export default futuresModule;
