<template>
    <v-dialog
        transition="dialog-bottom-transition"
        max-width="1024"
        v-model="isVisible"
        persistent
        scrollable
    >
        <template v-slot:default="dialog">
            <v-card>
                <v-card-title class="headline">
                    {{ $t('masterpassword') }}
                </v-card-title>

                <v-card-text>
                    {{ $t('masterpasswordInfo') }}
                    <v-form v-on:submit.prevent>
                        <v-text-field
                            :label="$t('masterpassword')"
                            :rules="[rulesMasterPWD, masterSame]"
                            placeholder="Provide a master password"
                            v-model="MPWD"
                            :disabled="!$store.getters.tos"
                            type="password"
                        ></v-text-field>
                    </v-form>
                    <v-form v-on:submit.prevent>
                        <v-text-field
                            :label="$t('masterpasswordRetype')"
                            :rules="[rulesMasterPWD, masterSame]"
                            placeholder="Retype your master password"
                            v-model="MPWD2"
                            :disabled="!$store.getters.tos"
                            type="password"
                        ></v-text-field>
                    </v-form>
                </v-card-text>
                <v-card-actions class="justify-end">
                    <v-btn
                        text
                        @click.stop="dialog.value = false"
                    >{{ $t('Close') }}</v-btn>
                    <v-btn
                        text
                        @click="handleSubmit"
                    >{{ $t('Confirm') }}</v-btn>
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>

<script>
    /*eslint no-undef: "off"*/
    import axios from 'axios';

    export default {
        name: 'masterPassword',
        data() {
            return {
                MPWD: '',
                MPWD2: ''
            }
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
                if(confirm(this.$t('masterSure'))) {
                    if(this.rulesMasterPWD(this.$data.MPWD) == true && this.masterSame() == true) {
                        axios.post(`/api/v1/auth/create`, {'pwd': this.$data.MPWD}, {headers: {'sk': sk}}).then(response => {
                            this.$store.commit('SET_TOKEN', response.data.token);
                            this.$store.commit('SET_AUTHENTICATION', response.data.authentication);
                            this.handleClose();
                            this.$data.MPWD = "";
                            this.$data.MPWD2 = "";
                        });
                    } else {
                        alert("Make sure you have entered a correct master password")
                    }
                }
            },
            rulesMasterPWD(value) {
                if (/^[\w\[\]`!@#$%\^&*()={}:;<>+'-]*$/.test(value)){
                    if(value && value.length > 9) {
                        return true;
                    }
                }
                return this.$i18n.t('ruleMPWD')
            },
            masterSame(){
                if(this.$data.MPWD == this.$data.MPWD2){
                    return true;
                }
                return this.$i18n.t('ruleMPWD2')
            }
        },
    }
</script>

<style lang="css" scoped>
.v-card {
    width: 100%;
}
</style>