<template>
    <v-card class="card" elevation="2" tile>
        <v-card-subtitle v-if="is_onine">
            <v-badge
                bottom
                dot
                color="green"
            >Online</v-badge>
        </v-card-subtitle>
        <v-card-subtitle v-else>            
            <v-badge
                bottom
                dot
                color="red"
            >Offline</v-badge>
        </v-card-subtitle>
    </v-card>
</template>

<script>
    export default {
        name:'is-online',
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
                    () => this.$store.dispatch("get_online"),
                    1000
                );
            }
        },
        beforeDestroy () {
            clearInterval(this.polling);
        },
        computed: {
            is_onine() {
                return this.$store.getters.online;
            }
        },
    }
</script>

<style lang="scss" scoped>
.card {
    width:100%;
    height: 50px;
}
</style>