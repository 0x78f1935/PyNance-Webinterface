<template>
    <v-footer app>
      <!-- -->
    </v-footer>
</template>

<script>
    import { price } from './utils';

    export default {
        name: 'global-footer',
        methods: {
            format_price(amount) {
                return price(amount, this.$store.getters.metrics);
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>