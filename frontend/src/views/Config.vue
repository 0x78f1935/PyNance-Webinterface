<template>
    <v-container fluid>
        <v-form v-on:submit.prevent>
            <v-row>
                <v-text-field
                    label="Coinmarketcal API-Key"
                    placeholder="coinmarketcal API-Key"
                    v-model="coinmarketcalApiKey"
                    autofocus
                ></v-text-field>
                <v-btn dark x-large color="accent" @click="setApiKeyCoinmarketcal"> SAVE </v-btn>
            </v-row>
        </v-form>
    </v-container>
</template>

<script>
    import axios from 'axios';

    export default {
        data: () => ({
            coinmarketcal: '',
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