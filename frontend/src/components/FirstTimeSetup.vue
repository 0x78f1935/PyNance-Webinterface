<template>
    <v-dialog
        transition="dialog-bottom-transition"
        max-width="1024"
        v-model="isVisible"
        fullscreen
        persistent
        scrollable
    >
        <v-card>
            <v-container fluid>
                <knightrider :txt="title"></knightrider>
            </v-container>

            <v-container fluid class="center-text">
                <template v-if="step == 0">
                    <p>Welcome to PyNance!</p>
                    <p>
                        It looks like your setup is working correctly! You are a few steps away removed from using PyNance!<br>
                        In order to keep your experience as easy as possible PyNance will ask you a couple of questions.<br>
                        The questions relates to features PyNance has to offer. A couple of features do require some extra steps to make them work.
                    </p>
                    <p>
                        Some questions can be skipped and can be configured at a later stage.<br>
                        Use the buttons below to navigate through the installation steps.
                    </p>
                </template>
                <template v-else-if="step == 1">
                    <v-container fluid>
                        <v-img class="center-img" height="375" width="420" src="../assets/stonks/terror.gif"></v-img>
                    </v-container>
                    <p>
                        This tool is not a money printing tool and contains risks. <br>
                        You are responsible for your own money and actions.
                    </p>
                    <p>
                        By using this tool you agree to take FULL responsibility of your own money. <br>
                        Even if this would mean missed opportunities caused by the algorithm of this bot or worse; losses. <br>
                        Be responsible, Only trade with money you can afford to lose.
                    </p>
                    <p>
                        By clicking Next you acknowledge the risks involved with crypto trading. <br>
                        Take chances, Make mistakes, Get messy.... To the moon!
                    </p>
                </template>
                <template v-else-if="step == 2">
                    <p>
                        You can only access the bot with your master password once set!<br>
                        This action cannot be reverted. Keep your password safe.
                    </p>
                    <v-form v-on:submit.prevent>
                        <v-text-field
                            label="Master Password"
                            :rules="[rulesMasterPWD, masterSame]"
                            placeholder="Provide a master password"
                            v-model="MPWD"
                            :disabled="!$store.getters.tos"
                            type="password"
                        ></v-text-field>
                    </v-form>
                    <v-form v-on:submit.prevent>
                        <v-text-field
                            label="Validate Master Password"
                            :rules="[rulesMasterPWD, masterSame]"
                            placeholder="Retype your master password"
                            v-model="MPWD2"
                            :disabled="!$store.getters.tos"
                            type="password"
                        ></v-text-field>
                    </v-form>
                </template>
                <template v-else-if="step == 3">
                    <p>
                        Would you like to see upcomming events? <a href="https://coinmarketcal.com/" target="_blank">coinmarketcal.com</a> provides amazing information on crypto.<br>
                        In order to enable news items you will need an API-key from <a href="https://coinmarketcal.com/" target="_blank">coinmarketcal.com</a>.<br>
                        Follow the next steps to obtain an API-key and provide it in the input field below:
                        <ul class="list-style">
                            <li>
                                <a href="https://coinmarketcal.com/en/developer/login" target="_blank">Register</a> an account on <a href="https://coinmarketcal.com/" target="_blank">coinmarketcal.com</a>
                            </li>
                            <li>Copy the API-Key from the CoinMarketCal dashboard</li>
                            <li>Past the API-Key in the input field below</li>
                        </ul>
                        <v-form v-on:submit.prevent>
                            <v-text-field
                                label="Coinmarketcal API-Key"
                                placeholder="coinmarketcal API-Key"
                                v-model="coinmarketcal"
                            ></v-text-field>
                        </v-form>
                    </p>
                </template>
                <template v-else-if="step == 4">
                    <p>
                        Thank you so much for using PyNance! A lot of work went into it.<br>
                        Make sure to leave a star on GitHub! Would be very much appriciated.<br>
                    </p>
                    <p>
                        You can hover over options to open-up tooltips! <br>
                        In the top left corner you will find the menu icon <v-icon small>mdi-menu</v-icon> which can be used to navigate through PyNance.<br>
                        If you get stuck make sure to visit the <v-icon small>mdi-help</v-icon> icon.
                    </p>

                    <p>
                        If you like my work, feel free to send a tip to my BTC wallet
                    </p>
                    <p>
                        <code>1HpywjQRi5jmpYxZXo32VAgVmyHZLacbJG</code>
                    </p>
                </template>

            </v-container>

            <v-divider></v-divider>

            <v-card-actions>
                <v-btn color="accent" v-if="step > 0" @click="previousPage">Previous</v-btn>
                <v-btn color="accent" 
                    v-if="step != finalStep-1" 
                    @click="nextPage" 
                    :disabled="step==2 && this.rulesMasterPWD(this.$data.MPWD) != true || step == 2 && this.masterSame() != true ? true : false"
                >{{ step == 1 ? "I acknowledge this disclaimer" : "Next" }}</v-btn>
                <v-btn color="accent" v-if="canSkip.includes(step)" @click="skipPage">Skip</v-btn>
                <v-btn color="accent" v-if="step == finalStep-1" @click="tearDown">Finish</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    import Knightrider from './Knightrider.vue';
    import axios from 'axios';

    export default {
        name: 'first-time-setup',

        data: () => ({
            step: 0,
            finalStep: 5,
            canSkip: [3],
            titles: ['Welcome!', 'Disclaimer', 'Configure Password', 'Cryptocurrency Calendar', 'Almost done!', 'Closing'],
            MPWD: '',
            MPWD2: '',
            coinmarketcal: '',
            passwordlength: 3
        }),

        components: {
            Knightrider,
        },
        computed: {
            isVisible() {
                return (this.$data.step < this.$data.finalStep && !this.$store.getters.authentication);
            },
            title(){
                return this.$data.titles[this.$data.step];
            }
        },
        methods: {
            handleClose() {
                this.$store.dispatch('loadDashboard');
            },
            previousPage(){
                if(this.$data.step > 0) {
                    this.$data.step -= 1;
                }
            },
            nextPage(){
                
                if (this.$data.step < this.$data.finalStep) {
                    if(this.$data.step == 1){
                        this.$store.commit('SET_TOS', true);
                        this.$data.step += 1;
                    }
                    else if(this.$data.step == 2) {
                        // Confirm password
                        if (confirm("Are you sure you want to set a master password, you will be unable to change this later")) {
                            if(this.rulesMasterPWD(this.$data.MPWD) == true) {
                                if(this.masterSame() == true) {
                                    axios.post(`/api/v1/system/create`, {'pwd': this.$data.MPWD}, {headers: {'sk': sk}}).then(response => {
                                        this.$store.commit('SET_VERSION', response.data.version);
                                        this.$store.commit('SET_LANGUAGE', response.data.language);
                                        this.$store.commit('SET_TOS', response.data.tos);
                                        this.$store.commit('SET_TOKEN', response.data.token);
                                        this.$data.MPWD = "";
                                        this.$data.MPWD2 = "";
                                        this.$data.step += 1;
                                    });
                                }
                            }
                        } 
                    }
                    else if(this.$data.step == 3) {
                        if(this.$data.coinmarketcal != ''){
                            axios.get(`/api/v1/coinmarketcal/check?api-key=${this.$data.coinmarketcal}`, {headers: {'token': this.$store.getters.token}}).then(response => {
                                if(response.data.error){
                                    alert('The provided API-Key seems to be invalid, please check your API key.');    
                                } else {
                                    this.$store.dispatch('SET_CONMARKETCAL', this.$data.coinmarketcal);
                                    this.$data.step += 1;
                                }
                            }).catch(resp => {
                                alert('The provided API-Key seems to be invalid, please check your API key.');
                            });
                        }
                    } else {
                        this.$data.step += 1;
                    }
                }
                console.log(this.$data.step)
            },
            skipPage() {
                this.$data.step += 1;
            },
            tearDown(){
                this.$data.step = this.$data.finalStep;
                this.$store.commit('SET_AUTHENTICATION', true);
            },
            rulesMasterPWD(value) {
                if (/^[\w\[\]`!@#$%\^&*()={}:;<>+'-]*$/.test(value)){
                    if(value && value.length >= this.$data.passwordlength) {
                        return true;
                    }
                }
                return `Create a password of atleast ${this.$data.passwordlength} characters`
            },
            masterSame(){
                if(this.$data.MPWD == this.$data.MPWD2){
                    return true;
                }
                return "Your master passwords are not the same";
            },
        },
    }
</script>

<style lang="scss" scoped>
.center-text {
    text-align: center;
}

.center-img {
    display: block;
    margin-left: auto;
    margin-right: auto 
}

.list-style{
    list-style: inside;
}
</style>