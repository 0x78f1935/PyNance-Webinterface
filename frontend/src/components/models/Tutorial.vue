<template>
    <v-dialog
        transition="dialog-bottom-transition"
        max-width="1024"
        v-model="isVisible"
    >
        <template v-slot:default="dialog">
            <v-card tile>
                <v-card-text>
                    <v-img
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_1.png')"
                        :src="require('../../assets/ui_1.png')"
                    ></v-img>
                    <b-container>
                        <p
                            v-for="(item, i) in tutorial_data"
                            :key="i"
                        >
                            {{item.number}}. {{ item.description }}
                        </p>
                    </b-container>

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
    function initialState (){
        return {
            loading: false,
            tutorial_data: [
                {"number": 1, "description": "This indicator shows if the bot is currently trading. All trades are halted when the bot is offline."},
                {"number": 2, "description": "If you would like to burn your eyes you could turn off dark mode."},
                {"number": 3, "description": "The two values selected will be glued together to form the symbol which the bot uses to trade."},
                {"number": 4, "description": "This percentage is the guaranteed profit margin the bot uses before the bot sells its coins."},
                {"number": 5, "description": "You can use this button to toggle the bot on/off."},
                {"number": 6, "description": "Before changing the settings, you need to unlock the settings by using this button. Changes have immediate effect."},
                {"number": 7, "description": "Displays the current status of the bot."},
                {"number": 8, "description": "You can use the search field to search through your order history."},
                {"number": 9, "description": "This is your order history. You can filter by clicking on the columns if you like too."},
            ],
            model: 1
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