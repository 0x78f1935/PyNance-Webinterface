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
                <v-container>
                    <knightrider txt="PyNance - Login"></knightrider>
                </v-container>
                <v-container>
                    <v-card-text>
                        <v-form v-on:submit.prevent>
                            <v-text-field
                                label="Master Password"
                                placeholder="Provide your master password"
                                v-model="MPWD"
                                type="password"
                            ></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions class="justify-end">
                        <v-btn
                            text
                            @click="handle"
                        >Confirm</v-btn>
                    </v-card-actions>
                </v-container>
            </v-card>
        </template>
    </v-dialog>
</template>

<script>
    import axios from 'axios';
    import Knightrider from './Knightrider.vue';

    export default {
        name:'login',
        data() {
            return {
                show: true,
                MPWD: '',
            }
        },
        components: {
            Knightrider,
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
        methods: {
            handle(){
                axios.post(`/api/v1/system/`, {'pwd': this.$data.MPWD}, {headers: {'token': this.$store.getters.token}}).then(response => {
                    if(Object.keys(response.data).includes(sk)){
                        this.$store.commit('SET_AUTHENTICATED', response.data[sk]);
                        this.$data.show = false;
                        this.$data.MPWD = "";
                        this.$store.dispatch('loadDashboard');
                    }
                });

            },
        },
    }
</script>

<style lang="scss" scoped>

</style>