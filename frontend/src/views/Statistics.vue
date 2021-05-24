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
                                        <v-slider min="0" max="50" value="50" readonly dense color="#00FFFF"></v-slider>
                                    </td>
                                    <td>Order placement</td>
                                </tr>
                                <tr v-if="isFuture">
                                    <td>
                                        <v-slider min="0" max="50" value="50" readonly dense color="#ff4081"></v-slider>
                                    </td>
                                    <td>Stop loss</td>
                                </tr>
                                <tr v-if="isFuture">
                                    <td>
                                        <v-slider min="0" max="50" value="50" readonly dense color="#00FF00"></v-slider>
                                    </td>
                                    <td>Take Profit</td>
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
                                        max="1000"
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
                    name: "ORDER PLACEMENT",
                    type: "EMA",
                    data: [ ],
                    settings: {
                        color: "#00FFFF"
                    }
                },
                {
                    name: "STOP LOSS",
                    type: "EMA",
                    data: [ ],
                    settings: {
                        color: "#ff4081"
                    }
                },
                {
                    name: "TAKE PROFIT",
                    type: "EMA",
                    data: [ ],
                    settings: {
                        color: "#00FF00"
                    }
                },
            ],
            tool: "Cursor",
            drawingMode: false,
            isVisible: true,
            status: {},
            polling: null,
            orders: {},
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
                this.updateKlines();
                this.updateOrders();
            }, 5000)
        },
        beforeDestroy () {
            clearInterval(this.polling);
        },
        methods: {
            updateKlines() {
                axios.get(`/api/v1/klines`, {headers: {'token': this.$store.getters.token}}).then(response => {
                    this.$data.title = response.data.symbol
                    if(response.data.order) {
                        this.$data.chart.data = response.data.klines.slice(1);
                        this.$data.onchart[0].data = response.data.klines.map(x => [x[0], response.data.price_target] ).slice(1);
                        this.$data.status = {
                            'target': response.data.symbol,
                            'current_target': response.data.price_target, 
                            'trade_type': response.data.trade_type,
                            'target_type': response.data.target_type,
                        }
                        if(response.data.trade_type == 'FUTURES') {
                            this.$data.status['position'] = response.data.position;
                            if(response.data.position == "LONG") {
                                this.$data.onchart[1].data = response.data.klines.map(x => [x[0], response.data.stop_loss] ).slice(1);
                                this.$data.onchart[2].data = response.data.klines.map(x => [x[0], response.data.take_profit] ).slice(1);
                                this.$data.status['stop_loss'] = response.data.stop_loss;
                                this.$data.status['take_profit'] = response.data.take_profit;
                            } else {
                                this.$data.onchart[1].data = response.data.klines.map(x => [x[0], response.data.take_profit] ).slice(1);
                                this.$data.onchart[2].data = response.data.klines.map(x => [x[0], response.data.stop_loss] ).slice(1);                                
                                this.$data.status['stop_loss'] = response.data.take_profit;
                                this.$data.status['take_profit'] = response.data.stop_loss;
                            }
                        }
                    }
                }).catch(e => console.log(e));
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
            isFuture() {
                if(this.$data.status.trade_type == 'FUTURES') { return true; }
                else { return false; }
            }
        }
    }
</script>

<style lang="scss" scoped>
table {
    background-color: #1E1E1E;
}
</style>