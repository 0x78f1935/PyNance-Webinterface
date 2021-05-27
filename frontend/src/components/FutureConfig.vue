<template>
    <v-container fluid>
        Trade configuration Futures
        <v-row align="center">
            <v-col cols="12">
                <v-combobox
                    :items="this.$store.getters.symbolsChoices"
                    v-model="selectedSymbols"
                    label="Symbols"
                    hint="Select symbols you would like to trade with PyNance"
                    persistent-hint
                    hide-selected
                    clearable
                    multiple
                    autofocus
                    deletable-chips
                    chips
                >
                </v-combobox>
            </v-col>
        </v-row>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    Expected leverage is {{$store.getters.expectedLeverage}}X if available otherwise it takes a leverage close to the expected leverage.
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-slider
                    v-model="expectedLeverage"
                    label="Expected Leverage"
                    thumb-color="accent"
                    thumb-label="always"
                    :thumb-size="16"
                    :hint="`Max 125x - Currently ${$store.getters.expectedLeverage}X`"
                    max="125"
                    min="1"
                    persistent-hint
                >
                    <template v-slot:append>
                        <v-text-field
                            v-model="expectedLeverage"
                            class="mt-0 pt-0"
                            type="number"
                            style="width: 60px"
                        ></v-text-field>
                    </template>
                </v-slider>
            </v-col>
        </v-row>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    Select the timeframe to use when calculating the average of the buy/sell volume ratio
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-select
                    :items="this.$store.getters.volumeTimeFrameSelection"
                    v-model="selectedVolumeTimeframe"
                    hint="The timeframe corresponds to the timeframe available in the graphs within Binance"
                    item-text="state"
                    item-value="abbr"
                    label="Select"
                    persistent-hint
                    return-object
                    single-line
                ></v-select>
            </v-col>
        </v-row>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    Total volume candles to take into account when calculating LONG or SHORT position
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-slider
                    v-model="totalVolume"
                    label="Total candles in volume to take into account"
                    thumb-color="accent"
                    thumb-label="always"
                    :thumb-size="16"
                    :hint="`Max 500 - Currently ${$store.getters.totalVolume}`"
                    max="500"
                    min="2"
                    persistent-hint
                >
                    <template v-slot:append>
                        <v-text-field
                            v-model="totalVolume"
                            class="mt-0 pt-0"
                            type="number"
                            style="width: 60px"
                        ></v-text-field>
                    </template>
                </v-slider>
            </v-col>
        </v-row>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    Set the selected margin type. ISOLATED is recommended.
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-select
                    :items="this.$store.getters.marginTypeChoices"
                    v-model="marginType"
                    hint="The timeframe corresponds to the timeframe available in the graphs within Binance"
                    item-text="state"
                    item-value="abbr"
                    label="Select"
                    persistent-hint
                    return-object
                    single-line
                ></v-select>
            </v-col>
        </v-row>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    When {{$store.getters.inGreen}}% in profit move stop-loss to increase secured profit
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-slider
                    v-model="inGreen"
                    label="Trailing Stop-Loss"
                    thumb-color="accent"
                    thumb-label="always"
                    :thumb-size="24"
                    :hint="`${$store.getters.inGreen}% profit to move SL`"
                    max="5"
                    min="0.1"
                    step=0.1
                    persistent-hint
                >
                    <template v-slot:append>
                        <v-text-field
                            v-model="inGreen"
                            class="mt-0 pt-0"
                            type="number"
                            style="width: 60px"
                        ></v-text-field>
                    </template>
                </v-slider>
            </v-col>
        </v-row>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    Allow going into negative numbers for {{$store.getters.inRed}}% (STOP-LOSS representation)
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-slider
                    v-model="inRed"
                    label="Negative tolerance"
                    thumb-color="accent"
                    thumb-label="always"
                    :thumb-size="24"
                    :hint="`${$store.getters.inRed}% negative tolerance, when 0% place stop-loss on buy entry`"
                    max="25"
                    min="0"
                    step=0.001
                    persistent-hint
                >
                    <template v-slot:append>
                        <v-text-field
                            v-model="inRed"
                            class="mt-0 pt-0"
                            type="number"
                            style="width: 60px"
                        ></v-text-field>
                    </template>
                </v-slider>
            </v-col>
        </v-row>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    The total amount of your wallet used on the selected symbol when placing a buy order
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-slider
                    v-model="walletAmount"
                    label="Wallet amount"
                    thumb-color="accent"
                    thumb-label="always"
                    :thumb-size="24"
                    :hint="`Max 100% - Currently ${$store.getters.walletAmount}%`"
                    max="99"
                    min="1"
                    persistent-hint
                >
                    <template v-slot:append>
                        <v-text-field
                            v-model="walletAmount"
                            class="mt-0 pt-0"
                            type="number"
                            style="width: 60px"
                        ></v-text-field>
                    </template>
                </v-slider>
            </v-col>
        </v-row>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    The take profit margin. When hit take profit (current price) +/- {{$store.getters.takeProfit}}%
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-slider
                    v-model="takeProfit"
                    label="Take Profit"
                    thumb-color="accent"
                    thumb-label="always"
                    :thumb-size="24"
                    :hint="`Max 100% - Currently ${$store.getters.takeProfit}%`"
                    max="100"
                    min="0.1"
                    step=0.1
                    persistent-hint
                >
                    <template v-slot:append>
                        <v-text-field
                            v-model="takeProfit"
                            class="mt-0 pt-0"
                            type="number"
                            style="width: 60px"
                        ></v-text-field>
                    </template>
                </v-slider>
            </v-col>
        </v-row>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    Apply SPOT strategy on-top of the futures stratagy
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-checkbox
                    v-model="spot_average"
                    :label="$store.getters.useAverage ? 'Dubble check average before placing any order' : 'Skipping extra average check, enable to configure'"
                ></v-checkbox>
            </v-col>
        </v-row>

        <v-container v-if="$store.getters.useAverage">
            <v-divider inset class="cdiv"></v-divider>
            <v-row align="center">
                <v-col cols="6">
                    <v-subheader>
                        Select the timeframe to use when calculating the lowest average for a buy order
                    </v-subheader>
                </v-col>

                <v-col cols="6">
                    <v-select
                        :items="this.$store.getters.timeframeChoices"
                        v-model="selectedTimeframe"
                        hint="The timeframe corresponds to the timeframe available in the graphs within Binance"
                        item-text="state"
                        item-value="abbr"
                        label="Select"
                        persistent-hint
                        return-object
                        single-line
                    ></v-select>
                </v-col>
            </v-row>
            <v-divider inset class="cdiv"></v-divider>
            <v-row align="center">
                <v-col cols="6">
                    <v-subheader>
                        Select the total amount of candles to take into account when calculating the lowest average for a buy order
                    </v-subheader>
                </v-col>

                <v-col cols="6">
                    <v-slider
                        v-model="candleInterval"
                        label="Amount of candles"
                        thumb-color="accent"
                        thumb-label="always"
                        :thumb-size="20"
                        :hint="`Max 1000 candles - Currently ${$store.getters.candleInterval} candles`"
                        max="1000"
                        min="2"
                        persistent-hint
                    >
                        <template v-slot:append>
                            <v-text-field
                                v-model="candleInterval"
                                class="mt-0 pt-0"
                                type="number"
                                style="width: 60px"
                            ></v-text-field>
                        </template>
                    </v-slider>
                </v-col>
            </v-row>

            <v-divider inset class="cdiv"></v-divider>
            <v-row align="center">
                <v-col cols="6">
                    <v-subheader>
                        The following value is used to suppress the lowest average price for a buy order by {{$store.getters.belowAverage}}%
                    </v-subheader>
                </v-col>

                <v-col cols="6">
                    <v-text-field
                        v-model="belowAverage"
                        label="Suppression"
                        :hint="`Lowest average - ${$store.getters.belowAverage}% = Max buy price`"
                        type="number"
                        persistent-hint
                    ></v-text-field>
                </v-col>
            </v-row>
        </v-container>

        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-btn
                    color="accent"
                    depressed
                    @click="save"
                >
                    <v-icon left>
                        mdi-content-save
                    </v-icon>
                    Save
                </v-btn>
            </v-col>

            <v-col cols="2">
                <v-switch
                    v-model="spot"
                    :label="$store.getters.spot ? 'Trading in Spot!' : 'Trading USDT-M futures!'"
                ></v-switch>
            </v-col>

            <v-col cols="2">
                <v-checkbox
                    v-model="sandbox"
                    :label="$store.getters.sandbox ? 'Sandbox-Mode enabled' : 'Sandbox-Mode disabled'"
                ></v-checkbox>
            </v-col>

            <v-col cols="2">
                <v-checkbox
                    v-model="multipleOrders"
                    :label="$store.getters.allowMultipleOrders ? 'Multiple positions allowed' : 'Multiple positions disallowed'"
                ></v-checkbox>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: 'futures-config',
        methods: {
            save() {
                if(confirm('Are you sure you would like to save your changes? PyNance will go offline after submitting changes, Remember to put PyNance back online!')){
                    this.$store.dispatch('toggleOnline', false);
                    this.$store.dispatch('saveTradeConfig');
                }
            },
        },
        computed: {
            expectedLeverage: {
                get() { return this.$store.getters.expectedLeverage },
                set(value) { this.$store.commit('SET_EXPECTED_LEVERAGE', value); }
            },
            selectedVolumeTimeframe: {
                get() { return this.$store.getters.volumeTimeFrame },
                set(value) { this.$store.commit('SET_VOLUME_TIME_FRAME', value); }
            },
            totalVolume: {
                get() { return this.$store.getters.totalVolume },
                set(value) { this.$store.commit('SET_TOTAL_VOLUME', value); }
            },
            activatePrice: {
                get() { return this.$store.getters.activatePrice },
                set(value) { this.$store.commit('SET_ACTIVATE_PRICE', value); }
            },
            inGreen: {
                get() { return this.$store.getters.inGreen },
                set(value) { this.$store.commit('SET_IN_GREEN', value); }
            },
            inRed: {
                get() { return this.$store.getters.inRed },
                set(value) { this.$store.commit('SET_IN_RED', value); }
            },
            moveStopLoss: {
                get() { return this.$store.getters.moveStopLoss },
                set(value) { this.$store.commit('SET_MOVE_STOP_LOSS', value); }
            },
            marginType: {
                get() { return this.$store.getters.marginType },
                set(value) { this.$store.commit('SET_MARGIN_TYPE', value); }
            },
            selectedSymbols: {
                get() { return this.$store.getters.symbols },
                set(value) { this.$store.commit('SET_SYMBOLS', value); }
            },
            totalTP: {
                get() { return this.$store.getters.totalTP },
                set(value) { this.$store.commit('SET_TOTAL_TP', value); }
            },
            takeProfit: {
                get() { return this.$store.getters.takeProfit },
                set(value) { this.$store.commit('SET_TAKE_PROFIT', value); }
            },
            spot_average: {
                get() { return this.$store.getters.useAverage },
                set(value) { this.$store.commit('SET_USE_AVERAGE', value); }
            },
            selectedTimeframe: {
                get() { return this.$store.getters.timeframe },
                set(value) { this.$store.commit('SET_TIMEFRAME', value); }
            },
            candleInterval: {
                get() { return this.$store.getters.candleInterval },
                set(value) { this.$store.commit('SET_CANDLE_INTERVAL', value); }
            },
            walletAmount: {
                get() { return this.$store.getters.walletAmount },
                set(value) { this.$store.commit('SET_WALLET_AMOUNT', value); }
            },
            belowAverage: {
                get() { return this.$store.getters.belowAverage },
                set(value) { this.$store.commit('SET_BELOW_AVERAGE', value); }
            },
            spot: { 
                get() { return this.$store.getters.spot },
                set(value) { 
                    if(value == false){
                        if(confirm("Are you sure you would like to enable USDT-M futures? USDT-M futures involves a higher risk, you could potentionally lose money with USDT-M futures.")){
                            this.$store.commit('SET_SPOT', false);
                        } else { 
                            this.$store.commit('SET_SPOT', true);
                        }
                    } else { this.$store.commit('SET_SPOT', value); }
                }
            },
            sandbox: {
                get() { return this.$store.getters.sandbox },
                set(value) { this.$store.commit('SET_SANDBOX', value); }
            },
            multipleOrders: {
                get() { return this.$store.getters.allowMultipleOrders },
                set(value) { this.$store.commit('SET_ALLOW_MULTIPLE_ORDERS', value); }
            },
        }
    }
</script>

<style lang="scss" scoped>
@media only screen and (max-width: 600px) {
    .cdiv {
        display: flex !important;
        margin-bottom: 50px !important;
        border-color: transparent !important;
    }
}
.cdiv {
    display: none;
    margin-bottom: 0px;
    border-color: transparent;
}
</style>