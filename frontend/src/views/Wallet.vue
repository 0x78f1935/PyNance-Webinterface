<template>
    <v-container fluid>
        <v-row>
            <v-col
                cols="12"
                md="12"
            >
                <v-text-field
                    :disabled="loading"
                    v-model="search"
                    label="Search for asset"
                >
                    <v-icon
                        slot="prepend"
                        color="accent"
                    >mdi-magnify
                    </v-icon>
                </v-text-field>
            </v-col>
            <v-progress-circular
                v-if="loading"
                indeterminate
                color="accent"
                class="mr-2 center"
            ></v-progress-circular>
            <v-col
                v-else
                v-for="coin, index in coins"
                :class="$store.getters.spot ? coin.coin.toUpperCase().includes(search.toUpperCase()) || coin.name.toUpperCase().includes(search.toUpperCase()) ? 'visible' : 'collapse' : coin.asset.toUpperCase().includes(search.toUpperCase()) ? 'visible' : 'collapse'"
                :key="index"
                cols="6"
                md="2"
            >
                <wallet-info
                    :ref="$store.getters.spot ? coin.coin : coin.asset"
                    :coinName="$store.getters.spot ? coin.coin : coin.asset"
                    :projectName="$store.getters.spot ? coin.name : ''"
                    :free="$store.getters.spot ? coin.free : coin.availableBalance"
                    :freezed="$store.getters.spot ? coin.freeze : 'Not used in Futures'"
                    :locked="$store.getters.spot ? coin.locked : 'Not used in Futures'"
                ></wallet-info>
            </v-col>
        </v-row>
            
    </v-container>
</template>

<script>
    import axios from 'axios';
    import walletInfo from '../components/walletInfo.vue';

    export default {
        components: { walletInfo },
        data() {
            return {
                status: 404,
                coins: [],
                loading: true,
                search: ''
            }
        },
        mounted () {
            axios.get(`/api/v1/wallet`, {headers: {'token': this.$store.getters.token}}).then(response => {
                this.$data.status = response.data.status;
                this.$data.coins = response.data.wallet;
                this.$data.loading = false;
            });
        },
    }
</script>

<style lang="scss" scoped>
.center {
    width: 100% !important;
    margin-left: auto;
    margin-right: auto;
}
</style>