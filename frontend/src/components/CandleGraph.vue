<template>
    <b-container v-if="this.$store.getters.candlesticks.length">
        <apexchart 
            :series="seriesEntries"
            :options="charOptions"
            width="100%"
            height="280px"
        ></apexchart>
    </b-container>
</template>

<script>
    export default {
        name: 'candle-graph',
        props: {
            card: {
                type: Boolean,
                default: false
            }
        },
        data() {
            return {
                charData: [],
                charOptions: {
                    chart: {
                        type: 'candlestick',
                        height: 350,
                        zoom: {
                            enabled: false,
                            type: 'x',  
                            autoScaleYaxis: false,
                            zoomedArea: {
                                fill: {
                                    color: '#90CAF9',
                                    opacity: 0.4
                                },
                                stroke: {
                                    color: '#0D47A1',
                                    opacity: 0.4,
                                    width: 1
                                }
                            }
                        }
                    },
                    title: {
                        text: this.$store.getters.symbol,
                        align: 'left'
                    },
                    xaxis: {
                        type: 'datetime',
                    },
                    yaxis: {
                        tooltip: {
                            enabled: true
                        }
                    },
                    responsive: [{
                        breakpoint: 1000,
                        options: {},
                    }],
                    theme: {
                        mode: this.$store.getters.darkmode ? 'dark' : 'light'
                    },
                },
            }
        },
        computed: {
            seriesEntries() {
                return [{
                    data:  this.$store.getters.candlesticks.map(item => { 
                        return {
                            x: new Date(item.opentime),
                            y: [
                                parseFloat(item.open),
                                parseFloat(item.high),
                                parseFloat(item.low),
                                parseFloat(item.close),
                            ]
                        }
                    })
                }];
            }
        }
    }
</script>