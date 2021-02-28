<template>
    <v-card class="card" elevation="2" tile>
        <v-card-subtitle>Currency 1: <span v-html="this.$store.getters.cur1"></span></v-card-subtitle>

            <v-card-text>
                <v-autocomplete
                    :disabled="!editing"
                    :items="this.$store.getters.symbols"
                    label="First Symbol"
                    v-model="cur1"
                ></v-autocomplete>

            </v-card-text>
            
            <v-divider></v-divider>

            <v-card-subtitle>Currency 2: <span v-html="this.$store.getters.cur2"></span></v-card-subtitle>

            <v-card-text>
                <v-autocomplete
                    :disabled="!editing"
                    :items="this.$store.getters.symbols"
                    label="Second Symbol"
                    v-model="cur2"
                ></v-autocomplete>

            </v-card-text>
        <v-divider></v-divider>

        <v-card-subtitle>Take Profit: <span v-html="this.$store.getters.take_profit"></span>%</v-card-subtitle>
        <v-card-text>
            <v-slider
                :disabled="!editing"
                v-model="tp"
                max="95"
                min="5"
                step="5"
                thumb-label
                ticks
                @click="$store.dispatch('get_take_profit')"
            ></v-slider>

        </v-card-text>
        
        
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
                >{{this.$store.getters.online ? "Go Offline" : "Go Online"}}</v-btn>
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

    export default {
        name: 'settings-panel',
        components: {
            HelpADevOut,
            Tutorial,
            Disclaimer
        },
        data() {
            return {
                editing: false,
                helpdev: false,
                tut: false,
                show_disclaimer: true
            }
        },
        created () {
            this.$store.dispatch("get_take_profit");
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
                this.$data.show_disclaimer = true;
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
            }
        },
    }
</script>

<style lang="scss" scoped>
.card {
    width: 100%
}
</style>