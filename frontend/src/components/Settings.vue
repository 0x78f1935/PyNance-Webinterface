<template>
    <v-card class="card" elevation="2" tile>
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
                    <v-icon>mdi-help</v-icon>
                </v-btn>

                <v-btn icon>
                    <v-icon>mdi-gift</v-icon>
                </v-btn>

                <v-btn
                    class="m-1"
                    elevation="2"
                    style="width:140px"
                    @click="$store.dispatch('toggle_online')"
                >{{this.$store.getters.online ? "Go Offline" : "Go Online"}}</v-btn>
            </v-flex>
            <v-flex class="text-xs-right" style="justify-content: flex-end; display:flex;margin-right:5px;">
                <v-btn icon @click="editing = !editing">
                    <v-icon v-if="editing">mdi-lock-open</v-icon>
                    <v-icon v-else>mdi-lock</v-icon>
                </v-btn>
            </v-flex>



        </v-card-actions>
    </v-card>
</template>


<script>
    export default {
        name: 'settings-panel',
        data() {
            return {
                editing: false
            }
        },
        created () {
            this.$store.dispatch("get_take_profit");
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
            }
        },
    }
</script>

<style lang="scss" scoped>
.card {
    width: 100%
}
</style>