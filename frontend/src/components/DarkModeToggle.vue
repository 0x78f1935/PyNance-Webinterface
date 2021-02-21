<template>
    <v-switch v-model="toggle_darkmode" hide-details :color="color"></v-switch>
</template>

<script>
    export default {
        name:'dark-mode-toggle',
        props: {
            color: {
                type: String,
                default: "indigo darken-3"
            },
        },
        computed: {
            toggle_darkmode: {
                get() {return this.$store.getters.darkmode; },
                set(value) {
                    this.$store.commit('SET_DARKMODE', value);
                    this.$vuetify.theme.dark = this.$store.getters.darkmode;
                }
            },
        },
    }
</script>

<style lang="scss" scoped>

</style>

