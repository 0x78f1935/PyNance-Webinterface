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
                        v-if="step=='1'"
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_1.png')"
                        :src="require('../../assets/ui_1.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='2'"
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_2.png')"
                        :src="require('../../assets/ui_2.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='3'"
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_3.png')"
                        :src="require('../../assets/ui_3.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='4'"
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_4.png')"
                        :src="require('../../assets/ui_4.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='5'"
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_5.png')"
                        :src="require('../../assets/ui_5.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='6'"
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_6.png')"
                        :src="require('../../assets/ui_6.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='7'"
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_7.png')"
                        :src="require('../../assets/ui_7.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='8'"
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_8.png')"
                        :src="require('../../assets/ui_8.png')"
                    ></v-img>
                    <v-img
                        v-else-if="step=='9'"
                        class="mt-5"
                        :lazy-src="require('../../assets/ui_9.png')"
                        :src="require('../../assets/ui_9.png')"
                    ></v-img>
                    <b-container>
                        <p
                            v-for="(item, i) in tutorial_data[$data.step]"
                            :key="i"
                        >
                            {{item.number}}. {{ item.description }}
                        </p>
                    </b-container>

                </v-card-text>
                <v-card-actions class="justify-end">
                    <v-btn
                        text
                        v-if="parseInt(step) > 1"
                        @click="previous_step"
                    >Previous</v-btn>
                    <v-btn
                        text
                        v-if="parseInt(step) < 9"
                        @click="next_step"
                    >Next</v-btn>
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
            tutorial_data: {
                "1": [
                    {"number": 1, "description": "If you would like to burn your eyes you could turn off dark mode."},
                    {"number": 2, "description": "Displays the current status of the bot."},
                    {"number": 3, "description": "Shows the current version of PyNance-Webinterface."},
                ],
                "2": [
                    {"number": 1, "description": "The two values configured here will be glued together to form the \"symbol\" which the bot uses to trade with."},
                    {"number": 2, "description": "If a symbol doesn't exists the bot will turn off and keeps the status 'offline'."},
                ],
                "3": [
                    {"number": 1, "description": "This percentage is the guaranteed profit margin the bot uses before the bot sells its coins."},
                    {"number": 2, "description": "The margin will also be used to calculate the quantity to buy coins with."},
                    {"number": 3, "description": "This configuration can only be edited when the configuration panel is unlocked"},
                ],
                "4": [
                    {"number": 1, "description": "You can unlock the configuration panel with the highlighted button"},
                    {"number": 2, "description": "Changes made when the control panel is unlocked take immediate effect."},
                    {"number": 3, "description": "When changes take place the bot will turn itself off with the offline status."},
                ],
                "5": [
                    {"number": 1, "description": "This indicator shows the online status of the bot."},
                    {"number": 2, "description": "You can turn the bot off/on by pressing the highlighted button."},
                ],
                "6": [
                    {"number": 1, "description": "Profits are shown in the top right corner."},
                    {"number": 2, "description": "Profits are calculated across all orders which the bot has placed."},
                    {"number": 3, "description": "Based on the total amount paid minus the total amount we sold it for."},
                ],
                "7": [
                    {"number": 1, "description": "In need to FOMO? The Panik button is just for you. (see highlighted button)."},
                    {"number": 2, "description": "When Panik is active the bot will sell of its tokens if the 'current price  is higher then the 'sell target without loss'."},
                    {"number": 3, "description": "When active it also prevents the bot from buying new tokens which allows you to go full FOMO."},
                ],
                "8": [
                    {"number": 1, "description": "The search bar allows you to quickly search through orders the bot has places previously."},
                    {"number": 2, "description": "Contains useful information about orders the bot has placed. The column 'Sell target with profit' is updated based on the 'Take Profit'."},
                ],
                "9": [
                    {"number": 1, "description": "If you like my work you could give me a follow, or share my content!"},
                    {"number": 2, "description": "Still in need to show more gratitude?, consider donating! That allows me to maintain such kind of projects."},
                ],
            },
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