<template>
    <v-card
        v-if="card"
        class="mt-4 mx-auto"
        max-width="600"
    >
        <v-sheet
            class="v-sheet--offset mx-auto"
            :color="this.$vuetify.theme.dark ? 'cyan' : 'red'"
            :elevation="this.$vuetify.theme.dark ? '12' : '0'"
            max-width="calc(100% - 32px)"
        >
            <v-sparkline
                :value="candledata"
                auto-line-width
                auto-draw
                color="white"
                line-width="2"
                padding="16"
            ></v-sparkline>
        </v-sheet>

        <v-card-text class="pt-0">
            <div class="title font-weight-light mb-2">
                {{ $t(evaluate) }}
            </div>

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
        name: 'spark-graph',
        props: {
            evaluate: {
                type: String,
                required: true
            },
            card: {
                type: Boolean,
                default: false
            }
        },
        computed: {
            candledata() {
                return this.$store.getters.candlesticks.map(x => parseFloat(x[this.$props.evaluate])*100000000)
            },
        },
    }
</script>
