<template>
    <v-dialog
        transition="dialog-bottom-transition"
        max-width="1024"
        v-model="isVisible"
        scrollable
        persistent
    >
        <template v-slot:default="dialog">
            <v-card>
                <v-card-text>
                    <v-card-title>
                        <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        :label="labelText"
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
                        :loading-text="loadingText"
                    ></v-data-table>
                    <small>{{ $t('donation_hint') }}</small>
                </v-card-text>
                <v-card-actions class="justify-end">
                    <v-btn
                        text
                        @click="dialog.value = false"
                    >{{ $t('Close') }}</v-btn>
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>

<script>
    function initialState (){
        return {
            loading: false,
            search: '',
            headers: [],
            items: [],
            data: [
                {'Wallet': 'BTC', 'Protocol': 'BTC', 'Address': '1HpywjQRi5jmpYxZXo32VAgVmyHZLacbJG'},
                {'Wallet': 'BTC', 'Protocol': 'BEP20 (BSC)', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'BTC', 'Protocol': 'BTC(SegWit)', 'Address': 'bc1qk7ke9trv36v7pjjaxvp6pekxkuwp8dtdnn6esv'},
                {'Wallet': 'ETH', 'Protocol': 'BEP20 (BSC)', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'ETH', 'Protocol': 'ERC20', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'USDT', 'Protocol': 'BEP20 (BSC)', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'USDT', 'Protocol': 'ERC20', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'USDT', 'Protocol': 'OMNI', 'Address': '1GwByNzvf9TfjFdAM3bmcK3x5KrpUoBVAa'},
                {'Wallet': 'USDT', 'Protocol': 'TRC20', 'Address': 'TPcfq8Abpu6w5SHAxM9P8wDHKvELuhw5bK'},
                {'Wallet': 'BNB', 'Protocol': 'BEP20 (BSC)', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
                {'Wallet': 'BNB', 'Protocol': 'ERC20', 'Address': '0xce4f2db8dbfe4dd9fd27f99111a6a23445f29f34'},
            ]
        }
    }

    export default {
        name: 'donate',
        computed: {
            isVisible: {
                get: function() {
                    return this.show;
                },
                set: function(newValue) {
                    if(newValue == false) { this.$emit('reset'); }
                }
            },
            labelText() {
                return this.$i18n.t('search');
            },
            loadingText() {
                return this.$i18n.t('loading');
            }
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
            handleClose() {
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