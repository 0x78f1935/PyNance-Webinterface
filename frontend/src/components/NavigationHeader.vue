<template>
    <v-app-bar app>
        <b-row>
            <b-col>
                <v-app-bar-nav-icon @click.stop="$store.dispatch('toggle_drawer', !$store.getters.drawer);"></v-app-bar-nav-icon>
            </b-col>
            <b-col class="mr-auro to_the_right">
                <profit-bar></profit-bar>
            </b-col>
        </b-row>
    </v-app-bar>
</template>

<script>
    import ProfitBar from '@/components/ProfitBar.vue';

    export default {
        name: 'nav-header',
        components: {
            ProfitBar,
        },
        computed: {
            drawer_mount: {
                get(){ return this.$store.getters.drawer; },
                set(value) { this.$store.dispatch('toggle_drawer', value); }
            }
        },
    }
</script>

<style lang="scss" scoped>
    .to_the_right {
        flex-direction: column-reverse;
        display: contents;
    }
</style>