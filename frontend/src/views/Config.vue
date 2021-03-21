<template>
  <b-container fluid>
    <h1>{{ $t('Configuration') }}</h1>

    <v-row>
        <v-col class="mt-2" cols="12">
            <strong>{{ $t('botSettings') }}</strong>
        </v-col>

        <v-col class="mt-2" cols="12">
            <small>{{ $t('targetSymbol') }}</small>
        </v-col>

        <v-col cols="6" md="2">
            <v-autocomplete
                :items="symbols"
                :label="$t('currency_1')"
                v-model="currency1"
                height="25"
                dense
                filled
                :disabled="!$store.getters.tos"
            ></v-autocomplete>
        </v-col>

        <v-col cols="6" md="1" class="center_content">
            <v-icon size="75">mdi-plus-thick</v-icon>
        </v-col>

        <v-col cols="6" md="2">
            <v-autocomplete
                :items="symbols"
                :label="$t('currency_2')"
                v-model="currency2"
                height="25"
                dense
                filled
                :disabled="!$store.getters.tos"
            ></v-autocomplete>
        </v-col>

        <v-col cols="6" md="2" class="equal">
            <v-icon size="50">mdi-equal</v-icon>
            {{ $store.getters.tos ? $store.getters.currency1 + $store.getters.currency2 : "Disabled" }}
        </v-col>

    </v-row>

    <v-row>
        <v-col class="mt-2" cols="12">
            <strong>{{ $t('buyEntry') }}</strong>
        </v-col>

        <v-col cols="6" md="2">

            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                    <img v-bind="attrs" v-on="on" v-else alt="timeframe" src="../assets/timeframe.png" height="150" class="image_max_size">
                </template>
                <span><small>{{ $t('timeintervalInfo') }}</small></span>
            </v-tooltip>

            <v-select
                :disabled="!$store.getters.tos"
                :items="timeframes"
                :label="$t('timeframe')"
                v-model="timeframe"
            ></v-select>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                        <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                        <img v-bind="attrs" v-on="on" v-else alt="timeframe" src="../assets/candles.png" height="150" class="image_max_size">
                </template>
                <span><small>{{ $t('averageInfo') }}</small></span>
            </v-tooltip>

            <v-autocomplete
                :items="Array.from({length: 1000}, (_, i) => i + 1)"
                :label="$t('candleinterval')"
                v-model="candles"
                :disabled="!$store.getters.tos"
            ></v-autocomplete>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount == 1" alt="stonk_1" src="../assets/stonks/1.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount > 1 && walletAmount < 10" alt="stonk_2" src="../assets/stonks/10.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount >= 10 && walletAmount < 20" alt="stonk_3" src="../assets/stonks/20.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount >= 20 && walletAmount < 25" alt="stonk_4" src="../assets/stonks/25.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount >= 25 && walletAmount < 40" alt="stonk_5" src="../assets/stonks/40.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount >= 40 && walletAmount < 50" alt="stonk_6" src="../assets/stonks/50.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount >= 50 && walletAmount < 60" alt="stonk_7" src="../assets/stonks/60.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount >= 60 && walletAmount < 80" alt="stonk_8" src="../assets/stonks/80.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount >= 80 && walletAmount < 100" alt="stonk_9" src="../assets/stonks/90.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="walletAmount == 100" alt="stonk_10" src="../assets/stonks/100.png" height="150" class="image_max_size">

                </template>
                <span><small>{{ $t('walletInfo') }}</small></span>
            </v-tooltip>

            <v-form v-on:submit.prevent>
                <v-text-field
                    :label="$t('walletAmount') + this.$store.getters.walletAmount + '%'"
                    :rules="[rulesWalletAmount]"
                    placeholder="No Data"
                    v-model="walletAmount"
                    :disabled="!$store.getters.tos"
                ></v-text-field>
            </v-form>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                    <img v-bind="attrs" v-else v-on="on" alt="average_distance" src="../assets/average_distance.png" height="150" class="image_max_size">

                </template>
                <span><small>{{ $t('averageDistanceInfo') }}</small></span>
            </v-tooltip>

            <v-form v-on:submit.prevent>
                <v-text-field
                    :label="$t('averageDistance') + this.$store.getters.averageDistance + '%'"
                    :rules="[rulesAverageDistance]"
                    placeholder="No Data"
                    v-model="averageDistance"
                    :disabled="!$store.getters.tos"
                ></v-text-field>
            </v-form>
        </v-col>

        <v-col class="mt-2" cols="12">
            <small>{{ $t('calcInfo') }}</small>
        </v-col>
    </v-row>

    <v-row>
        <v-col class="mt-2" cols="12">
            <strong>{{ $t('sellEntry') }}</strong>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                    <img v-bind="attrs" v-on="on" v-else alt="timeframe" src="../assets/min_profit.gif" height="150" class="image_max_size">
                </template>
                <span><small>{{ $t('tooltipMargin') }}</small></span>
            </v-tooltip>

            <v-form v-on:submit.prevent>
                <v-text-field
                    :label="$t('profitMargin') + this.$store.getters.minimalProfit + '%'"
                    :rules="[rulesProfitMargin]"
                    :placeholder="$t('noData')"
                    v-model="minimalProfit"
                    :disabled="!$store.getters.tos"
                ></v-text-field>
            </v-form>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                    <img v-bind="attrs" v-on="on" v-else-if="$store.getters.panik==false" alt="kalm" src="../assets/kalm.png" height="150" class="image_max_size">
                    <img v-bind="attrs" v-on="on" v-else-if="$store.getters.panik==true" alt="panik" src="../assets/panik.png" height="150" class="image_max_size">
                </template>
                <span><small>{{ $t('tooltipPanik') }}</small></span>
            </v-tooltip>

            <span class="label_centered" :style="$store.getters.panik ? 'color:#4CAF50;' : 'color:#ff4081;'">{{ $store.getters.panik ? 'Active' : 'Disabled'}}</span>
        </v-col>
    </v-row>

    <v-row>
        <v-col class="mt-2" cols="12">
            <strong>{{ $t('Backup') }}</strong>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                    <v-icon v-bind="attrs" v-on="on" v-else size="150" class="image_max_size">mdi-download</v-icon>
                </template>
                <span><small>{{ $t('tooltipDownload') }}</small></span>
            </v-tooltip>

            <v-btn class="label_centered" @click="downloadBackup" :disabled="backupping || !$store.getters.tos">{{ $t('Download') + " " + $t('backup') }}</v-btn>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="80"></v-sheet>
                    <v-icon v-bind="attrs" v-on="on" v-else size="80" class="image_max_size">mdi-backup-restore</v-icon>
                </template>
                <span><small>{{ $t('tooltipRestore') }}</small></span>
            </v-tooltip>

            <v-file-input
                accept=".pynance"
                :label="$t('Restore') + ' ' + $t('backup')"
                :disabled="backupping || !$store.getters.tos"
                v-model="backupfile"
                truncate-length="10"
            ></v-file-input>
            <v-btn class="label_centered" @click="restoreBackup" :disabled="backupping">{{ $t('Restore') + " " + $t('backup') }}</v-btn>
        </v-col>
    </v-row>

    <v-row>
        <v-col class="mt-2" cols="12">
            <strong>{{ $t('Security') }}</strong>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                    <v-icon v-bind="attrs" v-on="on" v-else size="150" class="image_max_size">mdi-lock-alert</v-icon>
                </template>
                <span><small>{{ $t('tooltipSecurity') }}</small></span>
            </v-tooltip>

            <v-btn class="label_centered" :disabled="!$store.getters.tos || $store.getters.authentication" @click="showMasterPWD=true">{{ $store.getters.authentication ? $t('pwdSetAlready') : $t('setPassword') }}</v-btn>
        </v-col>
    </v-row>

    <v-row>
        <v-col class="mt-2" cols="12">
            <strong>{{ $t('looksAndFeels') }}</strong>
        </v-col>

        <v-col cols="6" md="2">
            <v-sheet v-if="loading" height="150"></v-sheet>
            <img v-else-if="$vuetify.theme.dark" alt="moon" src="../assets/moon.png" height="150" class="image_max_size">
            <img v-else alt="sun" src="../assets/sun.png" height="150" class="image_max_size">
            <v-switch :disabled="!$store.getters.tos" v-model="toggleDarkmode" hide-details color="accent darken-3" :label="$t('darkmode')" dense class="switcher">
                <template v-slot:label>
                    <span class="input__label">{{ $t('darkmode') }}</span>
                </template>
            </v-switch>
        </v-col>

        <v-col cols="6" md="2">
            <v-sheet v-if="loading" height="150"></v-sheet>
            <img v-else-if="$i18n.locale=='en'" alt="en" src="../assets/flags/american.png" height="150" class="image_max_size">
            <img v-else-if="$i18n.locale=='fil'" alt="fil" src="../assets/flags/filipino.png" height="150" class="image_max_size">
            <img v-else-if="$i18n.locale=='fr'" alt="fr" src="../assets/flags/french.png" height="150" class="image_max_size">
            <img v-else-if="$i18n.locale=='nl'" alt="nl" src="../assets/flags/dutch.png" height="150" class="image_max_size">
            <img v-else alt="sun" src="../assets/flags/unknown.png" height="150" class="image_max_size">

            <v-autocomplete
                :disabled="!$store.getters.tos"
                :items="$store.getters.languages"
                :label="$t('language')"
                v-model="selectedLanguage"
                height="25"
            ></v-autocomplete>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                    <img v-bind="attrs" v-on="on" v-else alt="profit" src="../assets/center.png" height="150" class="image_max_size">
                </template>
                <span><small>{{ $t('tooltipProfit') }}</small></span>
            </v-tooltip>

            <v-autocomplete
                :disabled="!$store.getters.tos"
                :items="$store.getters.symbols"
                :label="$t('profitSymbol')"
                v-model="selectedProfit"
                height="25"
            ></v-autocomplete>
        </v-col>

        <v-col cols="6" md="2">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-sheet v-bind="attrs" v-on="on" v-if="loading" height="150"></v-sheet>
                    <v-icon v-bind="attrs" v-on="on" v-else-if="$store.getters.online==true" size="150" class="image_max_size">mdi-signal</v-icon>
                    <v-icon v-bind="attrs" v-on="on" v-else-if="$store.getters.online==false" size="150" class="image_max_size">mdi-signal-off</v-icon>
                </template>
                <span><small>{{ $t('tooltipOnline') }}</small></span>
            </v-tooltip>

            <span class="label_centered" :style="$store.getters.online ? 'color:#4CAF50;' : 'color:#ff4081;'">{{ $store.getters.online ? 'Online' : 'Offline'}}</span>
        </v-col>
    </v-row>

    <v-snackbar
      v-model="snackbar"
      :timeout="timeout"
    >
      {{ snackbarText }}

        <template v-slot:action="{ attrs }">
            <v-btn
                color="accent"
                text
                v-bind="attrs"
                @click="snackbar = false"
            >
                {{ $t('Close') }}
            </v-btn>
        </template>
    </v-snackbar>
    <masterpassword :show="showMasterPWD" @reset="showMasterPWD=false"></masterpassword>
  </b-container>
</template>

<script>
    import masterpassword from '@/models/masterpassword.vue';

    export default {
        data() {
            return {
                loading: true,
                backupping: false,
                backupfile: null,
                showMasterPWD: false,
                timeout: 5000,
                snackbar: false,
                snackbarText: ""
            }
        },
        mounted () {
            this.$i18n.locale = this.$store.getters.language;
            this.$data.loading = false;
        },
        components: {
            masterpassword,
        },
        methods: {
            showSnackbar(text, timeout){
                this.$data.timeout = timeout;
                this.$data.snackbarText = text;
                this.$data.snackbar = true;
                
            },
            rulesProfitMargin(value){
                if (/^[0-9.\-]*$/.test(value)){
                    if(value > 1) {
                        return true;
                    }
                }
                return this.$i18n.t('ruleHigherThan') + '1.'
            },
            rulesWalletAmount(value){
                if (/^[0-9\-]*$/.test(value)){
                    if(value > 0 && value <= 100) {
                        return true;
                    }
                }
                return this.$i18n.t('ruleWallet')
            },
            rulesAverageDistance(value){
                if (/^[+-]?\d+(\.\d+)?$/.test(value)){
                    if(value >= 0 && value <= 100) {
                        return true;
                    }
                }
                return this.$i18n.t('ruleAverageDistance')
            },
            downloadBackup() {
                this.$store.dispatch('getBackup');
                this.showSnackbar(this.$i18n.t('done'), this.$data.timeout);
            },
            restoreBackup() {
                this.$store.dispatch('restoreBackup', {
                    backup: this.$data.backupfile, 
                    callbackNotifier: this.showSnackbar, 
                    done: this.$i18n.t('done'), 
                    try: this.$i18n.t('tryAgain')});
            },
        },
        computed: {
            toggleDarkmode: {
                get() {return this.$store.getters.darkmode; },
                set(value) {
                    this.$store.commit('SET_DARKMODE', value);
                    this.$vuetify.theme.dark = this.$store.getters.darkmode;
                }
            },
            selectedLanguage: {
                get() {
                    return this.$i18n.locale;
                },
                set(value) {
                    this.$i18n.locale = value;
                    this.$store.dispatch('setLanguage', value);
                }
            },
            symbols() {
                return this.$store.getters.symbols;
            },
            timeframes() {
                return this.$store.getters.timeframes;
            },
            currency1: {
                get() {
                    return this.$store.getters.currency1;
                },
                set(value) {
                    this.$store.dispatch("setCurrency1", value);
                },
            },
            currency2: {
                get() {
                    return this.$store.getters.currency2;
                },
                set(value) {
                    this.$store.dispatch("setCurrency2", value);
                },
            },
            minimalProfit: {
                get() { return this.$store.getters.minimalProfit; },
                set(value) {
                    this.$store.dispatch("setMinimalProfit", value);
                }
            },
            walletAmount: {
                get() { return this.$store.getters.walletAmount; },
                set(value) {
                    this.$store.dispatch("setWalletAmount", value);
                }
            },
            timeframe: {
                get() { return this.$store.getters.timeframe; },
                set(value) {
                    this.$store.dispatch("setTimeframe", value);
                }
            },
            candles: {
                get() { return this.$store.getters.candles; },
                set(value) {
                    this.$store.dispatch("setCandles", value);
                }
            },
            averageDistance: {
                get() { return this.$store.getters.averageDistance; },
                set(value) {
                    this.$store.dispatch("setAverageDistance", value);
                }
            },
            selectedProfit: {
                get() { return this.$store.getters.selectedProfit; },
                set(value) {
                    this.$store.dispatch("setSelectedProfit", value);
                }
            },
        },
    }
</script>

<style lang="scss" scoped>
.image_max_size {
    max-width: 245px;
    width: 100%;
}

.center_content {
    justify-content: space-around;
    display: flex;
}

.equal {
    align-self: center;
    font-size: 24px;
}

.label_centered {
    width: 100%;
    justify-content: center;
    display: flex;
    margin-top:15px;
}
</style>
