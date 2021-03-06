<template>
    <label>{{ $t('profit') }}<strong>{{ profit }}</strong></label>
</template>

<script>
    export default {
        name: 'profit-bar',
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
                    () => this.$store.dispatch("get_profit"),
                    1000
                );
            }
        },
        beforeDestroy () {
            clearInterval(this.polling);
        },
        computed: {
            profit() {
                return this.$store.getters.profit;
            }
        },
    }
</script>

<style lang="scss" scoped>
label{
    margin: 25px;
}
</style>