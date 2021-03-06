<template>
    <v-card class="order-table">
        <v-card-title>
            <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            :label="$t('search')"
            single-line
            hide-details
            :disabled="loading"
            ></v-text-field>
        </v-card-title>
        <v-data-table
            dense
            :headers="$store.getters.orders.headers"
            :items="$store.getters.orders.data"
            :items-per-page="5"
            :search="search"
            class="elevation-1"
            :loading="loading"
            :loading-text="$t('loading')"
        ></v-data-table>
    </v-card>
</template>

<script>
    export default {
        name: 'order-history',
        data() {
            return {
                loading: true,
                search: '',
                headers: [],
                items: [],
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
                        this.$store.dispatch('get_orders');
                        this.$data.loading = false;
                    },
                    1000
                )
                
            }
        },
        beforeDestroy () {
            clearInterval(this.polling);
        }
    }
</script>

<style lang="scss" scoped>
.order-table {
    width: 100%;
}
</style>