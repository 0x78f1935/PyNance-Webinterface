<template>
    <v-dialog
        transition="dialog-bottom-transition"
        max-width="1024"
        v-model="isVisible"
        scrollable
    >
        <template v-slot:default="dialog">
            <v-card>
                <v-card-text>
                    <v-card-title>
                        <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        single-line
                        hide-details
                        :disabled="loading"
                        ></v-text-field>
                    </v-card-title>
                    <v-data-table
                    dense
                        :headers="headers"
                        :items="items"
                        :items-per-page="5"
                        :search="search"
                        class="elevation-1"
                        :loading="loading"
                        loading-text="Loading... Please wait"
                    ></v-data-table>
                    <small>Feel free to show some gratitude by donating/depositing a tip to any of the wallets above. Thank you!</small>
                </v-card-text>
                <v-card-actions class="justify-end">
                    <v-btn
                        text
                        @click="dialog.value = false"
                    >Close</v-btn>
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>

<script>
    function initialState (processorCallback){
        return {
            hint: '',
            loading: false,
            search: '',
            headers: [],
            items: [],
            data: [
                {'Wallet': 'BTC', 'Address': '1HpywjQRi5jmpYxZXo32VAgVmyHZLacbJG'},
                {'Wallet': 'ETH', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'USDT', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'BUSD', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'ADA', 'Address': 'DdzFFzCqrhsdxzkcwkaAbZF61FEDZKW9d7u4omn6dxCfXs36vgTPUX1FQeVcioEb4ipRxhMfRpRA8D4fuHb7BrHkFpJkjGP5MLymUMhn'},
                {'Wallet': 'LTC', 'Address': 'LVh3um66kNcdMoJGmniPQKedaa2Q1y1zCH'},
                {'Wallet': 'DOT', 'Address': '15G49J1vyitQxnTV842Fqqedf6Wa1ZnG4dqkZ7ktRFf5F54d'},
                {'Wallet': 'DOGE', 'Address': 'DHR7GuvhBTcojG8RoTPsZcwL2ZtCk5BA7Y'},
                {'Wallet': 'FTM', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'LINK', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
            ]
        }
    }

    export default {
        name: 'help-a-dev-out',
        computed: {
            isVisible: {
                get: function() {
                    return this.show;
                },
                set: function(newValue) {
                    if(newValue == false) { this.$emit('reset'); }
                }
            },
        },
        data() {
            return initialState(this.onProcessComplete)
        },
        props: {
            show: {
                type: Boolean,
                default: false
            },
        },
        created(){
            this.$data.headers = Object.keys(this.$data.data[0]).map(item => { 
                return {
                    text: item,
                    value: item,
                    sortable: true,
                    filterable: true
                } 
            });
            this.$data.items = this.$data.data;
        },
        methods: {
            closing() {
                Object.assign(this.$data, initialState());
            },
            handleSubmit(event) {
                event.preventDefault(); // Prevents closing (TODO)
                this.handleClose();
            },
            handleClose(forceClose=false) {
                if(forceClose != true)
                    if ( confirm("Are you sure you want to leave? Unsaved progress will be lost!") )
                        this.$emit('reset'); 
                    else
                        return; // Prevents closing
                else
                    this.$emit('reset');
            },
        },
    }
</script>

<style lang="css" scoped>
.v-card {
    width: 100%;
}
</style>