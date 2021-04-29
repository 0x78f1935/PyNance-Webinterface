<template>
    <v-row>
        <v-col
            class="mt-2"
            cols="12"
        >
            Test
        </v-col>
        <template v-for="n in 4">
        <v-col
            :key="n"
            class="mt-2"
            cols="12"
        >
            <strong>Category {{ n }}</strong>
        </v-col>

        <v-col
            v-for="j in 6"
            :key="`${n}${j}`"
            cols="6"
            md="2"
        >
            <v-sheet height="150"></v-sheet>
        </v-col>
        </template>
    </v-row>
</template>

<script>
    export default {
        name: 'coinmarketcal',
    }
</script>

<style lang="scss" scoped>

</style>