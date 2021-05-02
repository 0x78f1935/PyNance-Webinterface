<template>
    <v-container fluid>
        Statistics
        <v-row>
            <v-col col="9">
                <trading-vue 
                    app
                    :data="this.$data"
                    :titleTxt="title"
                    :class="isVisible?'visible':'collapse'"
                ></trading-vue>
            </v-col>
            <v-col col="3">
                <v-card
                    class="transition-fast-in-fast-out v-card--reveal"
                    style="height: 100%;"
                >
                    <v-card-text class="pb-0">

                    </v-card-text>

                        <v-row>
                            <v-col col="6">
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
                            </v-col>
                            <v-col col="6">
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
                            </v-col>
                    </v-row>
                </v-card>
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
            title: "LTCUSDT",
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
            polling: null
            // ohlcv: [],
        }),
        mounted () {
            if(/Android|webOS|iPhone|iPad|Mac|Macintosh|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) && window.screen.width <= 1000) {
                this.$data.isVisible = false;
            }
            this.updateKlines();
            this.polling = setInterval(() => {
                console.log('Fetching data');
                this.updateKlines();
            }, 3000)
        },
        beforeDestroy () {
            clearInterval(this.polling);
        },
        methods: {
            updateKlines() {
                axios.get(`/api/v1/klines`, {headers: {'token': this.$store.getters.token}}).then(response => {
                    // this.$data.ohlcv = response.data.klines;
                    this.$data.chart.data = response.data.klines;
                    this.$data.onchart[0].data = response.data.klines.map(x => [x[0], response.data.current_target] );
                    this.$data.title = response.data.target;
                    this.$data.onchart[0].name = response.data.target_type;
                    this.$data.status = response.data.status;
                });
                
            }
        },
    }
</script>

<style lang="scss" scoped>
table {
    background-color: #1E1E1E;
}
</style>