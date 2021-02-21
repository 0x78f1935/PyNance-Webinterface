<template>
    <v-autocomplete
        auto-select-first
        :items="matrics"
        :hint="hint"
        label="Current Metrics"
        v-model="selector"
    ></v-autocomplete>
</template>

<script>
    export default {
        name: 'metrics-selector',
        data() {
            return {
                matrics: ['EUR', 'USD']
            }
        },
        computed: {
            hint() {
                return `Currently selected: "${this.$store.getters.metrics}"`;
            },
            selector: {
                get() { return this.$store.getters.metrics; },
                set(value) {
                    this.$store.commit('SET_METRICS', value);
                }
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>