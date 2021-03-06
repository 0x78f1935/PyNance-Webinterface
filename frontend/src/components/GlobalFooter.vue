<template>
    <v-footer app>
        <b-col>
            {{ $t('version') }} {{$store.getters.version}}
        </b-col>
        <b-col class="mr-auro to_the_right">
            <language-selector></language-selector>
            <v-btn icon>
                <v-icon @click="show_discord=true">mdi-discord</v-icon>
            </v-btn>
            <v-btn icon>
                <v-icon @click="redirect_twitter">mdi-twitter</v-icon>
            </v-btn>
            <v-btn icon>
                <v-icon @click="redirect_github">mdi-github</v-icon>
            </v-btn>
        </b-col>
        <discord :show="show_discord" @reset="show_discord=false"></discord>
    </v-footer>
</template>

<script>
    import { price } from './utils';
    import Discord from '@/components/models/Discord.vue';
    import LanguageSelector from '@/components/LanguageSelector.vue';

    export default {
        name: 'global-footer',
        components: {
            Discord,
            LanguageSelector,
        },
        data() {
            return {
                show_discord: false
            }
        },
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