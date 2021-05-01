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
                    hint="Max 1000 candles"
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
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>