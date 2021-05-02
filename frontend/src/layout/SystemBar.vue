<template>
    <v-system-bar height="30" app fixed dense>
        <span>{{ message }}</span>
    </v-system-bar>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "systembar",
        data: () => ({
            polling: null,
            message: '',
            total_orders: 0,
            updated: new Date()
        }),
        mounted () {
            this.updateSysBar();
            this.polling = setInterval(() => {
                console.log('Fetching data');
                this.updateSysBar();
            }, 3000)
        },
        beforeDestroy () {
            clearInterval(this.polling);
        },
        methods: {
            updateSysBar() {
                axios.get(`/api/v1/logic/systembar`, {headers: {'token': this.$store.getters.token}}).then(response => {
                    this.$data.message = response.data.message;
                    this.$data.total_orders = response.data.total_orders;
                    this.$data.updated = new Date(response.data.updated);
                })
            }
        },
    }
</script>

<style scoped>
.v-system-bar {
    justify-content: center;
}
</style>