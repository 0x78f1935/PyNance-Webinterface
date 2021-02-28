<template>
    <b-container fluid>
        <v-btn block color="accent" @click="$store.dispatch('set_panik', !$store.getters.panik)">
            {{ $store.getters.panik ? "KALM" : "PANIK"}}
        </v-btn>
        <b-container fluid v-if="$store.getters.panik" class="panik">
            <v-img
                :src="require('../assets/panik.png')"
                width="160px"
                height="160px"
            ></v-img>
        </b-container>
    </b-container>
</template>

<script>
    export default {
        name:'panik',
    }
</script>

<style scoped>
.panik {
    display: flex;
    justify-content: center;
}
</style>