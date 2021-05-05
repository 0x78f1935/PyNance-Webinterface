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

            <v-col cols="6">
                <v-switch
                    v-model="spot"
                    :label="$store.getters.spot ? 'Trading in Spot!' : 'Trading USDT-M futures!'"
                ></v-switch>
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
            }
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