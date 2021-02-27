<template>
    <v-card>
        <v-card-title>
            <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
            :disabled="loading"
            ></v-text-field>
        </v-card-title>
        <v-data-table
            :headers="headers"
            :items="items"
            :items-per-page="5"
            :search="search"
            class="elevation-1"
            :loading="loading"
            loading-text="Loading... Please wait"
        ></v-data-table>
    </v-card>
</template>

<script>
    import axios from 'axios';

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
                        axios.get('/api/v1/orders').then(resp => {
                            if(resp.data.length > 0) {
                                this.$data.headers = Object.keys(resp.data[0]).map(item => { 
                                let value = '';
                                if (item == 'brought_price') { value = 'Brought Price'; }
                                else if (item == 'created') { value = 'Created'; }
                                else if (item == 'currency_1') { value = 'Currency 1'; }
                                else if (item == 'currency_2') { value = 'Currency 2'; }
                                else if (item == 'current') { value = 'Processing'; }
                                else if (item == 'quantity') { value = 'Quantity'; }
                                else if (item == 'sold_for') { value = 'Sold For'; }
                                else if (item == 'symbol') { value = 'Symbol'; }
                                else if (item == 'updated') { value = 'Updated'; }
            
                                return {
                                    text: value,
                                    value: item,
                                    sortable: true,
                                    filterable: true
                                } });
                                this.$data.items = resp.data;
                                this.$data.loading = false;
                            }
                        });

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

</style>