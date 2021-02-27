<template>
    <b-container fluid px-5>
        <v-switch v-model="toggle_darkmode" hide-details :color="color" :label="label" :dense="true" class="switcher">
            <template v-slot:label>
                <span class="input__label">{{ label }}</span>
            </template>
        </v-switch>
        <v-spacer></v-spacer>
    </b-container>
</template>

<script>
    export default {
        name:'dark-mode-toggle',
        props: {
            color: {
                type: String,
                default: "indigo darken-3"
            },
            label: {
                type: String,
                default: "Dark Theme",
            }
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
.switcher{
    height: 50px;
}
.input__label {
    margin-top: 4px;
}
</style>

