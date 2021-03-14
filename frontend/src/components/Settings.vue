<template>
    <v-card class="card" elevation="2" tile>
        <!-- <v-card-subtitle>{{ $t('currency1') }}<span v-html="this.$store.getters.cur1"></span></v-card-subtitle> -->
            <v-card-text class="sm">{{ $t('sell-config') }}</v-card-text>

            <v-card-text class="sm">
                <v-autocomplete
                    :disabled="!editing"
                    :items="this.$store.getters.symbols"
                    :label="$t('firstSymbol')"
                    v-model="cur1"
                ></v-autocomplete>

            </v-card-text>
            
            <v-divider></v-divider>

            <!-- <v-card-subtitle>{{ $t('currency2') }}<span v-html="this.$store.getters.cur2"></span></v-card-subtitle> -->

            <v-card-text class="sm">
                <v-autocomplete
                    :disabled="!editing"
                    :items="this.$store.getters.symbols"
                    :label="$t('secondSymbol')"
                    v-model="cur2"
                ></v-autocomplete>

            </v-card-text>
        <v-divider></v-divider>

        <v-card-text  class="sm">
            <v-text-field
                :label="$t('takeProfit') + this.$store.getters.take_profit + '%'"
                placeholder="Placeholder"
                filled
                :disabled="!editing"
                v-model="tp"
                @change="$store.dispatch('get_take_profit')"
            ></v-text-field>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-text  class="sm">
            <v-text-field
                :label="$t('totalEntry') + this.$store.getters.total_entry + '%'"
                placeholder="Placeholder"
                filled
                :disabled="!editing"
                v-model="total_entry"
                @change="$store.dispatch('get_total_entry')"
            ></v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-text class="sm">{{ $t('buy-in-config') }}</v-card-text>

        <v-card-text class="sm">
            <v-select
                :disabled="!editing"
                :items="chart_types"
                :label="$t('timerinterval')"
                v-model="selected_chart"
                @change="$store.dispatch('get_current_price')"
            ></v-select>

        </v-card-text>

        <v-divider></v-divider>

        <v-card-text class="sm">
            <v-autocomplete
                :disabled="!editing"
                :items="Array.from({length: 1000}, (_, i) => i + 1)"
                :label="$t('candleinterval')"
                v-model="total_candles"
                @change="$store.dispatch('get_current_price')"
            ></v-autocomplete>

        </v-card-text>

        <v-divider></v-divider>
        
        <panik></panik>

        <v-btn block color="accent" @click="show_disclaimer = true">
            {{ $t('disclaimer_txt') }}
        </v-btn>
        <v-card-actions>

            <v-flex>
                <v-btn icon>
                    <v-icon @click="tut = true">mdi-help</v-icon>
                </v-btn>

                <v-btn icon>
                    <v-icon @click="helpdev=true">mdi-gift</v-icon>
                </v-btn>

                <v-btn
                    class="m-1"
                    elevation="2"
                    @click="toggle_bot"
                >{{this.$store.getters.online ? $t('goOffline') : $t('goOnline')}}</v-btn>
            </v-flex>
            <v-flex class="text-xs-right" style="justify-content: flex-end; display:flex;margin-right:5px;">
                <v-btn icon @click="start_editing()">
                    <v-icon v-if="editing">mdi-lock-open</v-icon>
                    <v-icon v-else>mdi-lock</v-icon>
                </v-btn>
            </v-flex>



        </v-card-actions>
        <help-a-dev-out :show="helpdev" @reset="helpdev=false"></help-a-dev-out>
        <tutorial :show="tut" @reset="tut=false"></tutorial>
        <disclaimer :show="show_disclaimer" @reset="show_disclaimer=false"></disclaimer>
    </v-card>
</template>


<script>
    import HelpADevOut from '@/components/models/HelpADevOut.vue';
    import Tutorial from '@/components/models/Tutorial.vue';
    import Disclaimer from '@/components/models/Disclaimer.vue';
    import Panik from '@/components/Panik.vue';

    export default {
        name: 'settings-panel',
        components: {
            HelpADevOut,
            Tutorial,
            Disclaimer,
            Panik
        },
        data() {
            return {
                editing: false,
                helpdev: false,
                tut: false,
                show_disclaimer: true,
                chart_types: ['1m', '3m', '5m', '15m', '30m', '1H', '2H', '4H', '6H', '8H', '12H', '1D', '3D', '1W', '1M']
            }
        },
        created () {
            this.$store.dispatch("get_take_profit");
            this.$store.dispatch("get_total_entry");
            this.$store.dispatch("get_symbols");
            this.$store.dispatch("get_currencies");
            this.$store.dispatch("get_version");
            this.$store.dispatch("get_maintainer");
        },
        methods: {
            start_editing() {
                this.$data.editing = !this.$data.editing;
            },
            toggle_bot(){
                // this.$data.show_disclaimer = true;
                this.$store.dispatch('toggle_online');
            },
        },
        computed: {
            tp: {
                get() {
                    return this.$store.getters.take_profit;
                },
                set(value) {
                    if(this.editing){
                        this.$store.dispatch("set_take_profit", value);
                    }
                },
            },
            total_entry: {
                get(){ return this.$store.getters.total_entry; },
                set(value) {
                    if(this.editing) {
                        this.$store.dispatch("set_total_entry", value);
                    }
                }
            },
            cur1: {
                get() {
                    return this.$store.getters.cur1;
                },
                set(value) {
                    if(this.editing){
                        this.$store.dispatch("set_cur1", value);
                    }
                },
            },
            cur2: {
                get() {
                    return this.$store.getters.cur2;
                },
                set(value) {
                    if(this.editing){
                        this.$store.dispatch("set_cur2", value);
                    }
                },
            },
            selected_chart: {
                get() { return this.$store.getters.timerinterval; },
                set(value) {
                    if(this.editing) {
                        this.$store.dispatch('set_timerinterval', value);
                    }
                }
            },
            total_candles: {
                get() { return this.$store.getters.candlehistory; },
                set(value) {
                    if(this.editing) {
                        this.$store.dispatch('set_candleinterval', value);
                    }
                }
            }
        },
    }
</script>

<style lang="scss" scoped>
.card {
    width: 100%
}

.sm{
    height: 45px;
}
</style>