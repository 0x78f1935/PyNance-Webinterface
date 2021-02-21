<template>
    <v-app-bar app>
        <b-row>
            <b-col>
                <h5>Profits: {{ format_price(45665) }}</h5>
            </b-col>
            <b-col class="d-flex flex-row-reverse">
                <h5>Balance: {{ format_price(5100) }}</h5>
            </b-col>
        </b-row>
    </v-app-bar>
</template>

<script>
    import { price } from './utils';

    export default {
        name: 'nav-header',
        methods: {
            format_price(amount) {
                return price(amount, this.$store.getters.metrics);
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>