<template>
    <v-container fluid>
        Statistics
        <trading-vue :data="this.$data"></trading-vue>
    </v-container>
</template>

<script>
    import TradingVue from 'trading-vue-js'

    export default {
        components: {
            TradingVue,
        },
        data() {
            return {
                ohlcv: [
                    
                ]
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>