<template>
    <v-footer app>
        <b-col>
            Version: {{$store.getters.version}}
        </b-col>
        <b-col class="mr-auro to_the_right">
            <v-btn icon>
                <v-icon @click="redirect_twitter">mdi-twitter</v-icon>
            </v-btn>
            <v-btn icon>
                <v-icon @click="redirect_github">mdi-github</v-icon>
            </v-btn>
        </b-col>
    </v-footer>
</template>

<script>
    import { price } from './utils';

    export default {
        name: 'global-footer',
        methods: {
            format_price(amount) {
                return price(amount, this.$store.getters.metrics);
            },
            redirect_twitter() {
                window.open(this.$store.getters.twitter, '_blank');
            },
            redirect_github() {
                window.open(this.$store.getters.github, '_blank');
            },
        },
    }
</script>

<style lang="scss" scoped>
    .to_the_right {
        flex-direction: column-reverse;
        display: contents;
    }
</style>