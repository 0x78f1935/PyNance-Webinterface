<template>
    <v-card class="card" elevation="2" tile>
        <v-card-subtitle>Take Profit: <span v-html="this.$store.getters.take_profit"></span>%</v-card-subtitle>
        <v-card-text>
            <v-slider
                v-model="tp"
                max="95"
                min="5"
                step="5"
                thumb-label
                ticks
                @click="$store.dispatch('get_take_profit')"
            ></v-slider>
        </v-card-text>
    </v-card>
</template>

<script>
    export default {
        name:'take-profit',
        created () {
            this.$store.dispatch("get_take_profit");
        },
        computed: {
            tp: {
                get() {
                    return this.$store.getters.take_profit;
                },
                async set(value) {
                    await this.$store.dispatch("set_take_profit", value);
                    await this.$store.dispatch("get_take_profit");
                },
            }
        },
    }
</script>

<style lang="scss" scoped>
.card {
    width:100%;
    height: 100px;
}
</style>