<template>
    <b-container>
        <v-btn block :color="$store.getters.panik ? 'green' : 'accent'" @click="$store.dispatch('set_panik', !$store.getters.panik)">
            {{ $store.getters.panik ? "KALM" : "PANIK"}}
        </v-btn>
        <b-container fluid>
            <v-snackbar
                v-model="paniker"
                class="snack"
                centered
                timeout="-1"
                top
            >
                <v-img
                    :src="require('../assets/panik.png')"
                    width="160px"
                    height="160px"
                >{{ $t('selling_panik') }}</v-img>
            </v-snackbar>
        </b-container>
    </b-container>
</template>

<script>
    export default {
        name:'panik',
        data() {
            return {
                snackbar: false
            }
        },
        computed: {
            paniker: {
                get() { return this.$store.getters.panik; },
                set() {}
            }
        },
        mounted () {
            this.$store.dispatch('get_panik');
        },
    }
</script>

<style scoped>
.panik {
    display: flex;
    justify-content: center;
}

.snack {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
</style>