<template>
    <div>
        Trade
        <v-combobox
            :items="this.$store.getters.symbolsChoices"
            v-model="selectedSymbols"
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
        computed: {
            selectedSymbols: {
                get() { return this.$store.getters.symbols },
                set(value) {
                    this.$store.commit('SET_SYMBOLS', value);
                }
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>