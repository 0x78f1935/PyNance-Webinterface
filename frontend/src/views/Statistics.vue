<template>
    <v-container fluid>
        Statistics
        <v-row>
            <v-col cols="6">
                <trading-vue 
                    app
                    :data="this.$data"
                    :titleTxt="title"
                    :class="isVisible?'visible':'collapse'"
                ></trading-vue>
                <!-- <GChart
                    :settings="{ packages: ['corechart'] }"
                    type="CandlestickChart"
                    :data="chartData"
                    :options="chartOptions"
                /> -->
            </v-col>
            <v-col cols="2">
                <v-card
                    class="transition-fast-in-fast-out v-card--reveal"
                    style="height: 100%;"
                >
                    <v-card-text class="pb-0">

                    </v-card-text>
                    <table class="table table-dark">
                        <thead>
                            <tr>
                                <th>Status</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="item, index in Object.entries(status)" :key="index">
                                <td>{{ item[0] }}</td>
                                <td>{{ item[1] }}</td>
                            </tr>
                        </tbody>
                    </table>
                </v-card>
            </v-col>
            <v-col cols="2">
                <v-card
                    class="transition-fast-in-fast-out v-card--reveal"
                    style="height: 100%;"
                >
                    <v-card-text class="pb-0">
                    </v-card-text>
                        <table class="table table-dark">
                            <thead>
                                <tr>
                                    <th>Graph Legend</th>
                                    <th></th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>
                                        <v-slider min="0" max="50" value="50" readonly dense color="#1E90FF"></v-slider>
                                    </td>
                                    <td>Current price</td>
                                </tr>
                                <tr>
                                    <td>
                                        <v-slider min="0" max="50" value="50" readonly dense color="#ff4081"></v-slider>
                                    </td>
                                    <td>Order target</td>
                                </tr>
                            </tbody>
                        </table>
                </v-card>
            </v-col>
            <v-col cols="2" v-if="this.$store.getters.graph_type">
                <v-card
                    class="transition-fast-in-fast-out v-card--reveal"
                    style="height: 100%;"
                >
                    <v-card-text class="pb-0">

                    </v-card-text>
                    <table class="table table-dark">
                        <thead>
                            <tr>
                                <th>Graph options</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    <v-select
                                        :items="this.$store.getters.graph_type_choices"
                                        v-model="graph_type"
                                        hint="Timeframe"
                                        item-text="state"
                                        item-value="abbr"
                                        label="Select"
                                        persistent-hint
                                        return-object
                                        single-line
                                    ></v-select>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <v-slider
                                        v-model="graph_interval"
                                        label="Graph Interval"
                                        thumb-color="accent"
                                        thumb-label="always"
                                        :thumb-size="24"
                                        :hint="`Max 5000 - Currently ${$store.getters.graph_interval}`"
                                        max="5000"
                                        min="2"
                                        persistent-hint
                                    >
                                        <template v-slot:append>
                                            <v-text-field
                                                v-model="graph_interval"
                                                class="mt-0 pt-0"
                                                type="number"
                                                style="width: 60px"
                                            ></v-text-field>
                                        </template>
                                    </v-slider>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </v-card>
            </v-col>
            <v-col cols="12">
                <v-data-table
                    :headers="orders.headers"
                    :items="orders.body"
                    :items-per-page="5"
                    class="elevation-1"
                ></v-data-table>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import TradingVue from 'trading-vue-js'
    import axios from 'axios';

    export default {
        components: {
            TradingVue,
        },
        data: () => ({
            title: "BTCUSDT",
            chart: {   // Mandatory
                type: "Spline", // "<Candles|Spline>",
                data: [],
                settings: {
                    color: "#1E90FF"
                }
            },
            onchart: [
                {
                    name: "BUY TARGET",
                    type: "EMA",
                    data: [ ],
                    settings: {
                        color: "#ff4081"
                    }
                }
            ],
            tool: "Cursor",
            drawingMode: false,
            isVisible: true,
            status: {},
            polling: null,
            orders: {},
            // chartData: [
            // ],
            // chartOptions: {
            //     chart: {
            //         title: 'Loading',
            //         subtitle: '...',
            //     },
            //     series: {
            //         0:{color: 'black', visibleInLegend: false},
            //         1:{visibleInLegend: true},
            //         2:{visibleInLegend: false},
            //         3:{type: 'line', color: 'red', visibleInLegend: false},
            //         4:{type: 'line', color: 'red', visibleInLegend: false},
            //         5:{type: 'line', color: 'red', visibleInLegend: false}
            //     },
            //     bar: { groupWidth: '100%' }, // Remove space between bars.
            //     candlestick: {
            //         fallingColor: { strokeWidth: 0, fill: '#a52714' }, // red
            //         risingColor: { strokeWidth: 0, fill: '#0f9d58' }   // green
            //     }
            // }
        }),
        created () {
            this.$store.dispatch('getGraphInterval');
        },
        mounted () {
            if(/Android|webOS|iPhone|iPad|Mac|Macintosh|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) && window.screen.width <= 1000) {
                this.$data.isVisible = false;
            }
            this.updateKlines();
            this.updateOrders();
            this.polling = setInterval(() => {
                console.log('Fetching data');
                this.updateKlines();
                this.updateOrders();
            }, 1000)
        },
        beforeDestroy () {
            clearInterval(this.polling);
        },
        methods: {
            updateKlines() {
                axios.get(`/api/v1/klines`, {headers: {'token': this.$store.getters.token}}).then(response => {
                    this.$data.title = response.data.symbol
                    if(response.data.order) {
                        this.$data.chart.data = response.data.klines;
                        this.$data.onchart[0].data = response.data.klines.map(x => [x[0], response.data.price_target] );
                        this.$data.onchart[0].name = response.data.target_type;
                        this.$data.status = {
                            'target': response.data.symbol, 
                            'current_target': response.data.price_target, 
                            'trade_type': response.data.trade_type,
                            'target_type': response.data.target_type,
                        }
                        // this.$data.chartData = response.data.klines;
                        // this.$data.chartOptions.chart.title = response.data.symbol;
                        // this.$data.chartOptions.chart.subtitle = response.data.target_type;
                    }
                });
            },
            updateOrders() {
                axios.get(`/api/v1/history/orders`, {headers: {'token': this.$store.getters.token}}).then(response => {
                    if(response.data.length > 0) {
                        this.$data.orders = {
                            headers: Object.keys(response.data[0]).map(key => {return {
                                text: key, 
                                align: 'start', 
                                sortable: true, 
                                value: key
                            }}),
                            body: response.data
                        }
                    }
                })
            }
        },
        computed: {
            graph_type: {
                get() { return this.$store.getters.graph_type },
                set(value) { 
                    this.$store.dispatch('setGraph', {
                        'graph-type': value,
                        'graph-interval': this.$store.getters.graph_interval
                    }); 
                }
            },
            graph_interval: {
                get() { return this.$store.getters.graph_interval },
                set(value) { 
                    this.$store.dispatch('setGraph', {
                        'graph-type': this.$store.getters.graph_type,
                        'graph-interval': value
                    }); 
                }
            },
        }
    }
</script>

<style lang="scss" scoped>
table {
    background-color: #1E1E1E;
}
</style>