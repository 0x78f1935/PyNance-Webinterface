<template>
    <v-container fluid>
        Trade
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
                    min="1"
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
                    max="100"
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
                >
                </v-autocomplete>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    export default {
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
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>