<template>
    <v-container fluid>
        Trade configuration SPOT
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
        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    Set the minimal expected profit margin before placing a sell order
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-text-field
                    v-model="profitMargin"
                    label="Minimal profit margin"
                    :hint="`Current expected profit ${$store.getters.profitMargin}%`"
                    type="number"
                    persistent-hint
                ></v-text-field>
            </v-col>
        </v-row>
        <v-divider inset class="cdiv"></v-divider>
        <v-row align="center">
            <v-col cols="6">
                <v-subheader>
                    Show profits as {{ $store.getters.profitAs }}, this has no impact PyNance algorithm
                </v-subheader>
            </v-col>

            <v-col cols="6">
                <v-autocomplete
                    :items="this.$store.getters.assets"
                    v-model="profitAs"
                    label="Show profits as"
                    :hint="`Currently selected ${$store.getters.profitAs}`"
                    persistent-hint
                    :disabled="true"
                >
                </v-autocomplete>
            </v-col>

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

            <v-col cols="3">
                <v-switch
                    v-model="spot"
                    :label="$store.getters.spot ? 'Trading in Spot!' : 'Trading USDT-M futures!'"
                ></v-switch>
            </v-col>

            <v-col cols="3">
                <v-checkbox
                    v-model="sandbox"
                    :label="$store.getters.sandbox ? 'Sandbox-Mode enabled' : 'Sandbox-Mode disabled'"
                ></v-checkbox>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
        name: 'spot-config',
        methods: {
            save() {
                if(confirm('Are you sure you would like to save your changes? PyNance will go offline after submitting changes, Remember to put PyNance back online!')){
                    this.$store.dispatch('toggleOnline', false);
                    this.$store.dispatch('saveTradeConfig');
                }
            },
        },
        computed: {
            selectedSymbols: {
                get() { return this.$store.getters.symbols },
                set(value) { this.$store.commit('SET_SYMBOLS', value); }
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
            profitMargin: {
                get() { return this.$store.getters.profitMargin },
                set(value) { this.$store.commit('SET_PROFIT_MARGIN', value); }
            },
            profitAs: {
                get() { return this.$store.getters.profitAs },
                set(value) { this.$store.commit('SET_PROFIT_AS', value); }
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