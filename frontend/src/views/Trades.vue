<template>
    <v-container fluid>
        <v-row align="center" v-if="spot">
            <spot-config></spot-config>
        </v-row>
        <v-row align="center" v-else>
            <future-config></future-config>
        </v-row>
    </v-container>
</template>

<script>
import FutureConfig from '../components/FutureConfig.vue';
    import SpotConfig from '../components/SpotConfig.vue';
    export default {
        components: { 
            SpotConfig,
            FutureConfig
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
