<template>
    <v-system-bar height="30" app fixed dense>
        <infobar></infobar>
    </v-system-bar>
</template>

<script>
    import Infobar from '@/components/informationbar.vue';

    export default {
        name: "systembar",
        components: {
            Infobar,
        },
    }
</script>
