<template>
    <v-navigation-drawer app>
        <b-row>
            <is-online></is-online>
        </b-row>
        <b-row>
            <dark-mode-toggle style="float:right;"></dark-mode-toggle>
        </b-row>
        <b-row>
            <take-profit></take-profit>
        </b-row>
    </v-navigation-drawer>
</template>

<script>
    import DarkModeToggle from '@/components/DarkModeToggle.vue';
    import TakeProfit from '@/components/TakeProfit.vue';
    import IsOnline from '@/components/Online.vue';

    export default {
        name: 'nav-drawer',
        components: {
            DarkModeToggle,
            TakeProfit,
            IsOnline
        },
    }
</script>

<style lang="scss" scoped>

</style>