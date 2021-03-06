<template>
    <b-container fluid class="mt-3">
        <b-row>
            <small>{{ $t('cur11') }} {{ $store.getters.cur1 }} {{ $t('cur12') }} {{ $store.getters.coin_current_price }} {{ $t('cur13') }}.</small>
        </b-row>
        <b-row>
            <small>{{ $t('cur21') }} {{ $store.getters.cur2 }} {{ $t('cur22') }} {{ $store.getters.fiat_current_price }} {{ $t('cur23') }}.</small>
        </b-row>
        <b-row>
            <small>{{ $t('cur31') }} {{ $store.getters.current_quantity }}.</small>
        </b-row>
    </b-container>
</template>

<script>
    export default {
        name: 'current-fiat-coin-price',
        data() {
            return {
                polling: null
            }
        },
        created () {
            this.poller();
        },
        methods: {
            poller() {
                this.polling = setInterval(
                    () => this.$store.dispatch("get_current_coin_price"),
                    1000
                );
            }
        },
        beforeDestroy () {
            clearInterval(this.polling);
        }
    }
</script>

<style lang="scss" scoped>

</style>