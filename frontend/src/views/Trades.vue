<template>
    <v-container fluid>
        <v-row align="center" v-if="spot">
            <v-col class="customwidth">
                <current-prices></current-prices>
            </v-col>
            <v-col class="moveToTop">
                <spot-config></spot-config>
            </v-col>
        </v-row>
        <v-row align="center" v-else>
            <v-col class="customwidth">
                <current-prices></current-prices>
            </v-col>
            <v-col class="moveToTop">
                <future-config></future-config>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import FutureConfig from '../components/FutureConfig.vue';
    import SpotConfig from '../components/SpotConfig.vue';
    import CurrentPrices from '../components/CurrentPrices';
    export default {
        components: { 
            SpotConfig,
            FutureConfig,
            CurrentPrices
        },
        computed: {
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

<style scoped>
.moveToTop{
    align-self: start;
}
.customwidth{
    max-width: 500px;
}
</style>