<template>
    <span>{{ $store.getters.msg }}</span>
</template>

<script>
    export default {
        name:'infobar',
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
                            this.$store.dispatch("getMsg");
                            this.$store.dispatch("getOnline");
                            this.$store.dispatch("getProfit");
                        }
                    },
                    1000
                );
            }
        },
        beforeDestroy () {
            clearInterval(this.polling);
        },
    }
</script>
