<template>
    <v-app-bar app>
        <b-row>
            <b-col class="col-1 m-1" style="max-width: 120px;">
                <v-app-bar-nav-icon @click.stop="$store.dispatch('toggle_drawer', !$store.getters.drawer);"></v-app-bar-nav-icon>
            </b-col>
            <b-col>
            </b-col>
            <v-app-bar-nav-icon :disabled="true" class="small_song"><current-value></current-value></v-app-bar-nav-icon>
            <b-col class="mr-auro to_the_right">
                <profit-bar></profit-bar>
            </b-col>
        </b-row>
    </v-app-bar>
</template>

<script>
    import ProfitBar from '@/components/ProfitBar.vue';
    import CurrentValue from '@/components/CurrentValue.vue';

    export default {
        name: 'nav-header',
        components: {
            ProfitBar,
            CurrentValue
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

    .small_song {
        font-size: 12px;
        margin: auto;
        min-width: 150px;
    }
</style>