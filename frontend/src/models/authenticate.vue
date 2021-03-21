<template>
    <v-dialog
        transition="dialog-bottom-transition"
        max-width="1024"
        v-model="isVisible"
        fullscreen
        persistent
        scrollable
    >
        <template>
            <v-card>
                <knightrider></knightrider>
                <v-container>
                    <v-card-text>
                        <v-form v-on:submit.prevent>
                            <v-text-field
                                :label="$t('masterpassword')"
                                placeholder="Provide your master password"
                                v-model="MPWD"
                                type="password"
                            ></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions class="justify-end">
                        <v-btn
                            text
                            @click="handleSubmit"
                        >{{ $t('Confirm') }}</v-btn>
                    </v-card-actions>
                </v-container>
                <v-container class="center_content">
                    <v-icon size="150">mdi-lock-open</v-icon>
                </v-container>
            </v-card>
        </template>
    </v-dialog>
</template>

<script>
    /*eslint no-undef: "off"*/
    import axios from 'axios';
    import knightrider from '@/components/knightrider.vue';

    export default {
        name: 'masterPasswordInput',
        data() {
            return {
                MPWD: '',
                MPWD2: ''
            }
        },
        components: {
            knightrider,
        },
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
            handleSubmit(){
                axios.post(`/api/v1/auth/`, {'pwd': this.$data.MPWD}, {headers: {'token': this.$store.getters.token}}).then(response => {
                    if(Object.keys(response.data).includes(sk)){
                        this.$store.commit('SET_AUTHENTICATED', response.data[sk]);
                        this.$data.MPWD = "";
                    }
                });

            },
        },
    }
</script>

<style lang="css" scoped>
.v-card {
    width: 100%;
}

.center_content {
    justify-content: space-around;
    display: flex;
}
</style>