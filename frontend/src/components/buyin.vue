<template>
    <span :class="$store.getters.currentPrice < $store.getters.averagePrice ? 'green' : 'red'">
        <span style="float: right">1 {{ $store.getters.currency1 }} == {{ $store.getters.currentPrice }} {{ $store.getters.currency2 }}</span><br/>
        <span style="float: right">Buy-in entry for {{ $store.getters.currency1 }}</span><br/>
        <span style="float: right"><strong>&#60;</strong> {{ $store.getters.averagePrice }}</span>
    </span>
</template>

<script>
    export default {
        name: 'buyin',
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
                    () => {
                        if(this.$store.getters.authenticated)
                        {
                            this.$store.dispatch("getPrice");
                        }
                    },
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
.red {
    color: #ff4081;
    font-weight: bold;
}

.green {
    color: rgb(55, 245, 55);
    font-weight: bold;
}
</style>