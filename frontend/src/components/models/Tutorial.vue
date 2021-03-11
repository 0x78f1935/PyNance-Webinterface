<template>
    <v-dialog
        transition="dialog-bottom-transition"
        max-width="1024"
        v-model="isVisible"
    >
        <template v-slot:default="dialog">
            <v-card tile>
                <v-card-text>
                    <b-container fluid>

                    <v-img
                        v-if="step=='1'"
                        class="mt-5 foto"
                        :lazy-src="require('../../assets/ui_1.png')"
                        :src="require('../../assets/ui_1.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='2'"
                        class="mt-5 foto"
                        :lazy-src="require('../../assets/ui_2.png')"
                        :src="require('../../assets/ui_2.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='3'"
                        class="mt-5 foto"
                        :lazy-src="require('../../assets/ui_3.png')"
                        :src="require('../../assets/ui_3.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='4'"
                        class="mt-5 foto"
                        :lazy-src="require('../../assets/ui_4.png')"
                        :src="require('../../assets/ui_4.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='5'"
                        class="mt-5 foto"
                        :lazy-src="require('../../assets/ui_5.png')"
                        :src="require('../../assets/ui_5.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='6'"
                        class="mt-5 foto"
                        :lazy-src="require('../../assets/ui_6.png')"
                        :src="require('../../assets/ui_6.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='7'"
                        class="mt-5 foto"
                        :lazy-src="require('../../assets/ui_7.png')"
                        :src="require('../../assets/ui_7.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='8'"
                        class="mt-5 foto"
                        :lazy-src="require('../../assets/ui_8.png')"
                        :src="require('../../assets/ui_8.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='9'"
                        class="mt-5 foto"
                        :lazy-src="require('../../assets/ui_9.png')"
                        :src="require('../../assets/ui_9.png')"
                    ></v-img>
                    </b-container>
                    <b-container>
                        <p v-if="$data.step==1">1. {{$t('tut11')}}</p>
                        <p v-if="$data.step==1">2. {{$t('tut12')}}</p>
                        <p v-if="$data.step==1">3. {{$t('tut13')}}</p>
                        <p v-if="$data.step==2">1. {{$t('tut21')}}</p>
                        <p v-if="$data.step==2">2. {{$t('tut22')}}</p>
                        <p v-if="$data.step==3">1. {{$t('tut31')}}</p>
                        <p v-if="$data.step==3">2. {{$t('tut32')}}</p>
                        <p v-if="$data.step==3">3. {{$t('tut33')}}</p>
                        <p v-if="$data.step==4">1. {{$t('tut41')}}</p>
                        <p v-if="$data.step==4">2. {{$t('tut42')}}</p>
                        <p v-if="$data.step==4">3. {{$t('tut43')}}</p>
                        <p v-if="$data.step==5">1. {{$t('tut51')}}</p>
                        <p v-if="$data.step==5">2. {{$t('tut52')}}</p>
                        <p v-if="$data.step==6">1. {{$t('tut61')}}</p>
                        <p v-if="$data.step==6">2. {{$t('tut62')}}</p>
                        <p v-if="$data.step==6">3. {{$t('tut63')}}</p>
                        <p v-if="$data.step==7">1. {{$t('tut71')}}</p>
                        <p v-if="$data.step==7">2. {{$t('tut72')}}</p>
                        <p v-if="$data.step==7">3. {{$t('tut73')}}</p>
                        <p v-if="$data.step==8">1. {{$t('tut81')}}</p>
                        <p v-if="$data.step==8">2. {{$t('tut82')}}</p>
                        <p v-if="$data.step==9">1. {{$t('tut91')}}</p>
                        <p v-if="$data.step==9">2. {{$t('tut92')}}</p>
                    </b-container>

                </v-card-text>
                <v-card-actions class="justify-end">
                    <v-btn
                        text
                        v-if="parseInt(step) > 1"
                        @click="previous_step"
                    >{{ $t('previous') }}</v-btn>
                    <v-btn
                        text
                        v-if="parseInt(step) < 9"
                        @click="next_step"
                    >{{ $t('next') }}</v-btn>
                    <v-btn
                        text
                        @click="dialog.value = false"
                    >{{ $t('close') }}</v-btn>
                </v-card-actions>
            </v-card>
        </template>
    </v-dialog>
</template>

<script>
    function initialState (){
        return {
            loading: false,
            model: 1,
            step: "1"
        }
    }

    export default {
        name: 'tutorial',
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
            return initialState();
        },
        props: {
            show: {
                type: Boolean,
                default: false
            },
        },
        methods: {
            closing() {
                Object.assign(this.$data, initialState());
            },
            handleSubmit(event) {
                event.preventDefault(); // Prevents closing (TODO)
                this.handleClose();
            },
            previous_step(){
                let value = parseInt(this.$data.step) - 1;
                this.$data.step = value.toString();
            },
            next_step(){
                let value = parseInt(this.$data.step) + 1;
                this.$data.step = value.toString();
            },
            handleClose(forceClose=false) {
                if(forceClose != true)
                {
                    if ( confirm(this.$i18n.t('leave_unsaved')) ) {
                        this.$data.step = "1";
                        this.$emit('reset'); 

                    } else { return; } // Prevents closing
                }
                else {
                    this.$data.step = "1";
                    this.$emit('reset');
                }
            },
        },
    }
</script>

<style scoped>
.foto{
    margin-top: 15px;
}
</style>