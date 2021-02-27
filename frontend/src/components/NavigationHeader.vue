<template>
    <v-app-bar app>
        <b-row>
            <b-col>
                <v-app-bar-nav-icon @click.stop="$store.dispatch('toggle_drawer', !$store.getters.drawer);"></v-app-bar-nav-icon>
            </b-col>
        </b-row>
    </v-app-bar>
</template>

<script>

    export default {
        name: 'nav-header',
        computed: {
            drawer_mount: {
                get(){ return this.$store.getters.drawer; },
                set(value) { this.$store.dispatch('toggle_drawer', value); }
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>