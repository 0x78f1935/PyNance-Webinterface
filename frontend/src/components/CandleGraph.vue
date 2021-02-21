<template>
    <v-card
        v-if="card"
        class="mt-4 mx-auto"
        max-width="600"
    >
        <v-sheet
            class="v-sheet--offset mx-auto"
            color="cyan"
            elevation="12"
            max-width="calc(100% - 32px)"
        >
            <v-sparkline
                :label="evaluate"
                :value="candledata"
                auto-draw
                color="white"
                line-width="2"
                padding="16"
            ></v-sparkline>
        </v-sheet>

        <v-card-text class="pt-0">
            <div class="title font-weight-light mb-2">
                {{ evaluate }}
            </div>
            <v-divider class="my-2"></v-divider>

        </v-card-text>
    </v-card>
    <v-sparkline
        v-else
        :value="candledata"
        auto-draw
    ></v-sparkline>
</template>

<script>
    export default {
        name: 'candle-graph',
        props: {
            updateCandles: { // When True it will fetch the data. to prevent being rate limited
                type: Boolean,
                default: false
            },
            evaluate: {
                type: String,
                required: true
            },
            card: {
                type: Boolean,
                default: false
            }
        },
        created () {
            if(this.$props.updateCandles == true) {
                setInterval(
                    () => { this.$store.dispatch('get_candlesticks') },
                    1000
                )
            }
        },
        computed: {
            candledata() {
                return this.$store.getters.candlesticks.map(x => parseFloat(x[this.$props.evaluate])*100000000)
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>