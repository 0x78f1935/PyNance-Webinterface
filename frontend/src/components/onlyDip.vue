<template>
    <v-btn block :color="$store.getters.only_dip ? 'green' : 'accent'" @click="$store.dispatch('set_only_dip', !$store.getters.only_dip)">
        {{ $store.getters.only_dip ? 'Buy Big DIP' : 'Buy Small DIP' }}
    </v-btn>
</template>

<script>
    export default {
        name:'only-dip',
        mounted () {
            this.$store.dispatch('get_only_dip');
        },
    }
</script>