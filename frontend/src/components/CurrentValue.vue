<template>
    <span>
        1 {{ $store.getters.cur1 }} == {{ $store.getters.current_price }} {{ $store.getters.cur2 }}
    </span>
</template>

<script>
    export default {
        name: 'current-value',
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
                    () => this.$store.dispatch("get_current_price"),
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