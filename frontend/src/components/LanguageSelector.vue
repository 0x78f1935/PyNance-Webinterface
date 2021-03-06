<template>
    <v-autocomplete
        class="languager"
        :items="langs"
        :label="$t('languages')"
        v-model="selected_language"
        height="15"
    ></v-autocomplete>
</template>

<script>
    export default {
        name: 'language-selector',
        computed: {
            selected_language: {
                get() {
                    return this.$i18n.locale;
                },
                set(value) {
                    this.$i18n.locale = value;
                    this.$store.commit('SET_LANGUAGE', value);
                }
            },
            langs() {
                return [...this.$store.getters.languages].sort();
            }
        },
    }
</script>

<style lang="scss" scoped>
.languager {
    max-width: 100px;
}
</style>

<style lang="scss">
.languager div.v-input__control {
    height: 15px;
}
</style>