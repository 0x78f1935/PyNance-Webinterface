<template>
    <b-container fluid>
        <v-btn block color="accent" @click="$store.dispatch('set_panik', !$store.getters.panik)">
            PANIK
        </v-btn>
        <b-container fluid v-if="$store.getters.panik">
            <v-img
                :src="require('../assets/panik.png')"
                width="100%"
            ></v-img>
        </b-container>
    </b-container>
</template>

<script>
    export default {
        name:'panik',
    }
</script>
