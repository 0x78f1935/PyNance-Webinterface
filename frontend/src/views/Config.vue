<template>
    <v-container fluid>
        <v-form v-on:submit.prevent>
            <v-row>
                <v-text-field
                    v-model="coinmarketcalApiKey"
                    :append-icon="showCoinmarketcal ? 'mdi-eye-off' : 'mdi-eye'"
                    append-outer-icon="mdi-content-save"
                    :type="showCoinmarketcal ? 'text' : 'password'"
                    name="input-10-1"
                    label="Coinmarketcal API-Key"
                    hint="Get yours at https://coinmarketcal.com/en/api"
                    autofocus
                    @click:append="showCoinmarketcal = !showCoinmarketcal"
                    @click:append-outer="setApiKeyCoinmarketcal"
                ></v-text-field>
            </v-row>

            <backup></backup>
        </v-form>
    </v-container>
</template>

<script>
    import axios from 'axios';
    import backup from '@/components/Backup.vue';

    export default {
        components: { backup },
        data: () => ({
            coinmarketcal: '',
            showCoinmarketcal: false
        }),
        computed: {
            coinmarketcalApiKey: {
                get(){
                    if (this.$data.coinmarketcal == '' && this.$store.getters.coinmarketcal != ''){
                        return this.$store.getters.coinmarketcal;
                    } else {
                        return this.$data.coinmarketcal;
                    }
                },
                set(value) {
                    this.$data.coinmarketcal = value;
                },
            }
        },
        methods: {
            setApiKeyCoinmarketcal() {
                if (this.$data.coinmarketcal != ''){
                    axios.get(`/api/v1/coinmarketcal/check?api-key=${this.$data.coinmarketcal}`, {headers: {'token': this.$store.getters.token}}).then(response => {
                        if(response.data.error){
                            alert('The provided API-Key seems to be invalid, please check your API key.');    
                        } else {
                            this.$store.dispatch('coinmarketcal', this.$data.coinmarketcal);
                            alert('The provided API-Key for coinmarketcal seems valid, API key saved!.');
                            this.$store.dispatch('loadKeys');
                        }
                    }).catch(resp => {
                        alert('The provided API-Key seems to be invalid, please check your API key.');
                    });
                }
            }
        },
    }
</script>

<style lang="scss" scoped>

</style>