<template>
    <v-autocomplete
        auto-select-first
        :items="symbols"
        :hint="hint"
        label="Current Symbol"
        v-model="autoselect"
    ></v-autocomplete>
</template>

<script>
    export default {
        name: 'symbol-selector',
        props: {
            frmt: {
                type: String,
                default: 'coins'
            },
        },
        created () {
            this.$store.dispatch('get_symbols', this.frmt);
        },
        computed: {
            symbols() {
                return this.$store.getters.symbols;
            },
            hint() {
                return `Currently selected: "${this.$store.getters.symbol}"`;
            },
            autoselect: {
                get() { return this.$store.getters.symbol; },
                set(value) {
                    this.$store.commit('SET_SYMBOL', value);
                }
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>