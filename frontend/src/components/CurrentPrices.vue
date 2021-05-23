<template>
    <v-card
        :loading="isLoading"
        class="mx-auto"
    >
    <template slot="progress">
        <v-progress-linear
            color="accent"
            height="10"
            indeterminate
        ></v-progress-linear>
    </template>

        <v-card-title>Current Prices</v-card-title>
        <v-card-text>
            <v-text-field
                :disabled="isLoading"
                v-model="search"
                label="Search for symbol"
            >
                <v-icon
                    slot="append"
                    color="accent"
                >mdi-magnify
                </v-icon>
            </v-text-field>

            <v-text-field
                v-model="quantity"
                label="Quantity"
                type="number"
                presists-hint
                hint=""
            ></v-text-field>
        </v-card-text>
        <v-card-text>
            <v-simple-table 
                v-if="!isLoading"
                fixed-header
                dense
                dark
            >
                <template v-slot:default>
                    <thead>
                        <tr>
                            <th 
                                v-for="column, index in Object.keys($store.getters.prices[0]).map(x => x.charAt(0).toUpperCase() + x.slice(1))" 
                                :key="`column_${index}`"
                            >{{ column }}</th>
                            <th>{{quantity}} cost(s)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="row, row_index in $store.getters.prices" 
                            :key="`row_${row_index}`"
                            :class="search.length > 0 && search != '' && row.symbol.toUpperCase().includes(search.toUpperCase()) ? 'visible' : search.length <= 0 && search == '' ? 'visible' : 'collapse'"
                        >
                            <td
                                v-for="item, item_index in Object.values(row)" 
                                :key="`item_${item_index}`"
                            >
                                {{ item }}
                            </td>
                            <td v-if="quantity == 1">{{ row.price }}</td>
                            <td v-else>{{ precise(row.price * quantity) }}</td>
                        </tr>
                    </tbody>
                </template>
            </v-simple-table>
        </v-card-text>
    </v-card>
</template>

<script>
    export default {
        name: "current-prices",
        data: () => ({
            polling: null,
            search: '',
            quantity: 1,
        }),
        mounted () {
            this.$store.dispatch('fetchPrices');
            this.polling = setInterval(() => {
                console.log('Fetching prices');
                this.$store.dispatch('fetchPrices');
                // this.test();
            }, 5000)
        },
        beforeDestroy () {
            clearInterval(this.polling);
        },
        methods: {
            test() {
                if(this.$store.getters.prices.length > 0) {
                    debugger;
                }
            },
            precise(x) {
                return Number.parseFloat(x).toPrecision(8);
            }
        },
        computed: {
            isLoading() {
                if(this.$store.getters.prices.length <= 0) { return true; }
                else { return false; }
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>