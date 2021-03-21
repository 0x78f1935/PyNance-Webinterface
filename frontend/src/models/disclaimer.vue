<template>
    <v-dialog
        transition="dialog-bottom-transition"
        v-model="isVisible"
        max-width="650"
        overlay-color="red"
        overlay-opacity="0.2"
    >
        <v-card
            tile
            class="mx-auto"
            min-width="450"
        >
            <template slot="progress">
                <v-progress-linear
                    color="deep-purple"
                    height="10"
                    indeterminate
                ></v-progress-linear>
            </template>

            <v-img height="375" src="../assets/stonks/terror.gif"></v-img>

            <v-card-title class="small_title">{{ $t('Disclaimer') }}</v-card-title>

            <v-card-text class="small_font">
                <v-row>
                    <v-container fluid>
                        {{ $t('disclaimerDesc1') }}
                    </v-container>
                </v-row>
                <v-row>
                    <v-container fluid>
                        {{ $t('disclaimerDesc2') }}
                    </v-container>
                </v-row>
                <v-row>
                    <v-container fluid>
                        {{ $t('takeChances') }}
                    </v-container>
                </v-row>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>

            <v-card-actions>
                <b-checkbox dense class="agreement" v-model="agreementCheck">{{ $t('disclaimerAgree') }}</b-checkbox>
            </v-card-actions>

            <v-divider class="mx-4"></v-divider>
            <v-card-text>
                <v-row>
                    <v-container fluid>
                        {{ $t('outsideClose') }}
                    </v-container>
                </v-row>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script>
    export default {
        name: 'disclaimer',
        computed: {
            isVisible: {
                get: function() {
                    return this.show;
                },
                set: function(newValue) {
                    if(newValue == false) { this.$emit('reset'); }
                }
            },
            agreementCheck: {
                get(){ return this.$store.getters.tos; },
                set(value){
                    this.$store.dispatch('setTos', value);
                }
            }
        },
        props: {
            show: {
                type: Boolean,
                default: false
            },
        },
        methods: {
            handleClose() {
                this.$emit('reset');
            },
        },
    }
</script>

<style scoped>
.center_content {
    display: flex;
    justify-content: center;
}

.small_title {
    font-size: 14px !important;
}

.small_font {
    font-size: 12px !important;
}

.yellowright {
    color: #fffb00;
    margin: 15px;
    text-align: center;
    font-size: 18px;
}
</style>