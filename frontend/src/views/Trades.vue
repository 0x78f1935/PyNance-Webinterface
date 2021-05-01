<template>
    <div>
        Trade
        <v-combobox
            :items="this.$store.getters.symbolsChoices"
            v-model="value"
            label="Symbols"
            hint="Select symbols you would like to trade with PyNance"
            persistent-hint
            hide-selected
            clearable
            multiple
            autofocus
            deletable-chips
            chips
        >
        </v-combobox>

    </div>
</template>

<script>
    export default {
        data: () => ({
            value: [],
        }),
    }
</script>

<style lang="scss" scoped>

</style>