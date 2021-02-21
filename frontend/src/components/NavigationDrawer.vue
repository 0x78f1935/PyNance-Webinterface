<template>
    <v-navigation-drawer app>
        <h1>PyNance</h1>
        <dark-mode-toggle style="float:right;"></dark-mode-toggle>
        <symbol-selector></symbol-selector>
        <metrics-selector></metrics-selector>
    </v-navigation-drawer>
</template>

<script>
    import SymbolSelector from './SymbolSelector';
    import MetricsSelector from './MetricsSelector';
    import DarkModeToggle from './DarkModeToggle.vue';

    export default {
        name: 'nav-drawer',
        components: {
            SymbolSelector,
            MetricsSelector,
            DarkModeToggle,
        },
    }
</script>

<style lang="scss" scoped>

</style>