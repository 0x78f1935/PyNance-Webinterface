<template>
    <v-app-bar app>
      <h1>PyNance</h1>
      <dark-mode-toggle></dark-mode-toggle>
    </v-app-bar>
</template>

<script>

    import DarkModeToggle from './DarkModeToggle.vue';

    export default {
        name: 'nav-header',
        components: {
            DarkModeToggle
        },
    }
</script>

<style lang="scss" scoped>

</style>