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
                    <iframe style="margin-top: 25px" src="https://discord.com/widget?id=817537111350968330&theme=dark" width="100%" height="480px" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
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
    export default {
        name: 'discord',
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

<style lang="css" scoped>
.v-card {
    width: 100%;
}
</style>