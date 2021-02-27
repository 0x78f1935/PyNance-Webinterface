<template>
    <v-card class="card" elevation="2" tile>
        <v-card-subtitle>Take Profit: {{ value }}%</v-card-subtitle>
        <v-card-text>
            <v-slider
                v-model="value"
                step="10"
                thumb-label
                ticks
            ></v-slider>
        </v-card-text>
    </v-card>
</template>

<script>
    export default {
        name:'take-profit',
        data() {
            return {
                value: 20
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