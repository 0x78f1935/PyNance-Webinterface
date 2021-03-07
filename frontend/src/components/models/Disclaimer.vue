<template>
    <v-dialog
        transition="dialog-bottom-transition"
        max-width="850"
        v-model="isVisible"
    >
        <template>
            <v-card tile class="card">
                <v-card-text>
                    <p class='yellowright' v-html="$t('disclaimer')"></p>
                </v-card-text>
            </v-card>
        </template>
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
.card {
    background: #ff404a;
}

.yellowright {
    color: #fffb00;
    margin: 15px;
    text-align: center;
    font-size: 18px;
}
</style>