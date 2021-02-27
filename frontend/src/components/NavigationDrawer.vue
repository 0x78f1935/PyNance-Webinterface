<template>
    <v-navigation-drawer app>
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
    }
</script>

<style lang="scss" scoped>

</style>