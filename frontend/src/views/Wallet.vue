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
                    @change="searching"
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
                :key="index"
                cols="6"
                md="2"
            >
                <wallet-info
                    :ref="coin.coin"
                    :coinName="coin.coin"
                    :projectName="coin.name"
                    :free="coin.free"
                    :freezed="coin.freeze"
                    :locked="coin.locked"
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
        methods: {
            searching() {
                for(let i = 0; i < Object.keys(this.$refs).length; i++){
                    if(Object.keys(this.$refs)[i].includes(this.$data.search)){
                        console.log('Match', Object.keys(this.$refs)[i]);
                        this.$refs[Object.keys(this.$refs)[i]][0].toggle(true);
                    } else {
                        console.log('NO Match', Object.keys(this.$refs)[i]);
                        this.$refs[Object.keys(this.$refs)[i]][0].toggle(false);
                    }
                }
            }
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