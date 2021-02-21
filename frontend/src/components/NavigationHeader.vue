<template>
    <v-app-bar app>
      <h1>PyNance</h1>
      <dark-mode-toggle></dark-mode-toggle>
      <symbol-selector></symbol-selector>
    </v-app-bar>
</template>

<script>

    import DarkModeToggle from './DarkModeToggle.vue';
    import SymbolSelector from './SymbolSelector';

    export default {
        name: 'nav-header',
        components: {
            DarkModeToggle,
            SymbolSelector
        },
    }
</script>

<style lang="scss" scoped>

</style>