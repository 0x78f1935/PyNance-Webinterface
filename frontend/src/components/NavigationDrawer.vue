<template>
    <v-navigation-drawer app v-model="drawer_mount">
        <b-row>
            <is-online></is-online>
        </b-row>
        <b-row>
            <dark-mode-toggle style="float:right;"></dark-mode-toggle>
        </b-row>
        <b-row>
            <settings-panel></settings-panel>
        </b-row>
    </v-navigation-drawer>
</template>

<script>
    import DarkModeToggle from '@/components/DarkModeToggle.vue';
    import SettingsPanel from '@/components/Settings.vue';
    import IsOnline from '@/components/Online.vue';

    export default {
        name: 'nav-drawer',
        components: {
            DarkModeToggle,
            SettingsPanel,
            IsOnline
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

</style>