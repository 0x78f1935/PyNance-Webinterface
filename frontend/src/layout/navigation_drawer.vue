<template>
    <v-navigation-drawer
      v-model="drawer"
      app
      class="pt-4"
    >
    <knightrider class="application_title"></knightrider>
    <b-row>
        <v-chip
            class="ma-2 button"
            color="accent"
            label
            @click="$store.dispatch('setDisclaimer', !$store.getters.disclaimer)"
        >
            {{ $t('Disclaimer') }}
        </v-chip>
        <b-checkbox dense class="agreement" v-model="agreementCheck">{{ $t('disclaimerAgree') }}</b-checkbox>
    </b-row>
    <v-divider></v-divider>

    <v-list dense nav id="nav" :disabled="!$store.getters.tos">
        <router-link to="/">
            <v-list-item link>
                <v-list-item-icon>
                    <v-icon>mdi-chart-line</v-icon>
                    <v-list-item-content>
                        <v-list-item-title>{{ $t('Orders') }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item-icon>

            </v-list-item>
        </router-link>

        <router-link to="/config">
            <v-list-item link>
                <v-list-item-icon>
                    <v-icon>mdi-cog</v-icon>
                    <v-list-item-content>
                        <v-list-item-title>{{ $t('Configure') }}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item-icon>

            </v-list-item>
        </router-link>
    </v-list>

    <v-divider></v-divider>
    <b-row>
        <v-chip
            class="ma-2 button"
            :color="$store.getters.online ? 'green' : 'accent'"
            label
            @click="$store.dispatch('setOnline', !$store.getters.online)"
            :disabled="!$store.getters.tos"
        >{{ $t('Online') }}</v-chip>

        <v-chip
            class="ma-2 button"
            :color="$store.getters.panik ? 'green' : 'accent'"
            label
            @click="$store.dispatch('setPanik', !$store.getters.panik)"
            :disabled="!$store.getters.tos"
        >{{ $t('Panik') }}</v-chip>
    </b-row>
    <v-divider></v-divider>

    <v-list dense nav id="nav">
        <v-list-item link @click="redirectGithub">
            <v-list-item-icon>
                <v-icon>mdi-github</v-icon>
                <v-list-item-content>
                    <v-list-item-title>{{ $t('github') }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item-icon>
        </v-list-item>

        <v-list-item link @click="redirectTwitter">
            <v-list-item-icon>
                <v-icon>mdi-twitter</v-icon>
                <v-list-item-content>
                    <v-list-item-title>{{ $t('twitter') }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item-icon>
        </v-list-item>

        <v-list-item link @click="showDiscord=true">
            <v-list-item-icon>
                <v-icon>mdi-discord</v-icon>
                <v-list-item-content>
                    <v-list-item-title>{{ $t('discord') }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item-icon>
        </v-list-item>
    </v-list>

    <v-divider></v-divider>
    <b-row>
        <v-chip
            class="ma-2 button"
            :color="$store.getters.online ? 'green' : 'accent'"
            label
            @click="showDonation=true"
        >{{ $t('Donate') }}</v-chip>

        <v-chip
            v-if="$store.getters.authentication"
            :disabled="!$store.getters.tos"
            class="ma-2 button"
            color="accent"
            label
            @click="$store.commit('SET_AUTHENTICATED', false);"
        >{{ $t('Lock') }}</v-chip>
    </b-row>

    <disclaimer :show="$store.getters.disclaimer" @reset="$store.dispatch('setDisclaimer', false)"></disclaimer>
    <discord :show="showDiscord" @reset="showDiscord=false"></discord>
    <donation :show="showDonation" @reset="showDonation=false"></donation>
    </v-navigation-drawer>
</template>

<script>
    import knightrider from '@/components/knightrider.vue';
    import Disclaimer from '@/models/disclaimer.vue';
    import Discord from '@/models/discord.vue';
    import Donation from '@/models/donation.vue';

    export default {
        name: 'drawer',
        components: {
            knightrider,
            Disclaimer,
            Discord,
            Donation
        },
        data() {
            return {
                showDiscord: false,
                showDonation: false
            }
        },
        methods: {
            redirectTwitter() {
                window.open(this.$store.getters.twitter, '_blank');
            },
            redirectGithub() {
                window.open(this.$store.getters.github, '_blank');
            },
        },
        computed: {
            drawer: {
                get(){ return this.$store.getters.drawer; },
                set(value) { this.$store.dispatch('toggleDrawer', value); }
            },
            agreementCheck: {
                get(){ return this.$store.getters.tos; },
                set(value){
                    this.$store.dispatch('setTos', value);
                }
            }
        },
    }
</script>

<style lang="scss" scoped>
    .application_title {
        justify-content: space-around;
        display: flex;
        margin: 0px;
    }

    .row {
        justify-content: space-evenly;
    }

    .button {
        width: 100%;
    }

    #nav {
        a {
            font-weight: bold;
            color: #ff4081;
            text-decoration: none;

            &.router-link-exact-active {
            color: #42b983;
            }
        }
    }

    .agreement {
        margin-top: 0px;
        padding-top: 0px;
    }

</style>