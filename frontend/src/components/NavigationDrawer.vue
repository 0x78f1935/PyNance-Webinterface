<template>
    <v-navigation-drawer app>
        <dark-mode-toggle style="float:right;"></dark-mode-toggle>
    </v-navigation-drawer>
</template>

<script>
    import DarkModeToggle from './DarkModeToggle.vue';

    export default {
        name: 'nav-drawer',
        components: {
            DarkModeToggle,
        },
    }
</script>

<style lang="scss" scoped>

</style>