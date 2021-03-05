<template>
    <v-dialog
        transition="dialog-bottom-transition"
        max-width="850"
        v-model="isVisible"
    >
        <template>
            <v-card tile class="card">
                <v-card-text>
                    <p class='yellowright'>
                        <strong>DISCLAIMER: This tool is not a money printing tool. You </strong> are <strong> responsible</strong> for <strong>your own money.</strong> <br/>
                        <strong>By using this tool you agree to take FULL responsibility of your own money. </strong> <br/>
                        Even if this means missed opportunities caused by the automation algorithm of this bot or worse, losses caused by this bot. <br/>
                        <strong>Be responsible</strong>, Only trade with money you can afford to lose. Take chances, Make mistakes, Get messy. To the moon! <br/>
                        <i>Tap outside this window to close this message</i>
                    </p>
                </v-card-text>
            </v-card>
        </template>
    </v-dialog>
</template>

<script>
    function initialState (){
        return {
            loading: false,
        }
    }

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

<style scoped>
.card {
    background: #ff404a;
}

.yellowright {
    color: #fffb00;
}
</style>