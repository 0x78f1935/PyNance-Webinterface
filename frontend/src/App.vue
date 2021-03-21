<template>
  <v-app id="inspire">
    <nav-header></nav-header>
    <drawer class="laden"></drawer>

    <v-main app>
      <systembar></systembar>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>

    <v-footer app>
      <b-col cols="11"></b-col>
      <b-col class="mr-auro to_the_right" cols="1" md="1">
        {{ $t('version') }}{{ $store.getters.version }}
      </b-col>
    </v-footer>

    <masterPasswordInput :show="!$store.getters.authenticated" @reset="$store.commit('SET_AUTHENTICATED', true)"></masterPasswordInput>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import Drawer from '@/layout/navigation_drawer.vue';
import NavHeader from '@/layout/navigation_header.vue';
import Systembar from '@/layout/navigation_system.vue';
import MasterPasswordInput from '@/models/authenticate.vue';

export default Vue.extend({
  name: 'App',

  components: {
    Drawer,
    NavHeader,
    Systembar,
    MasterPasswordInput
  },

  created: async function() {
    await this.$store.dispatch('initApp');
    this.$vuetify.theme.dark = this.$store.getters.darkmode;
  },

  data: () => ({
    drawer: true,
  }),
});
</script>

<style scoped>
  .laden {
      padding-top: 0px !important;
  }

  .to_the_right{
    justify-content: flex-end;
    display: flex;
  }
</style>

<style>
::-webkit-scrollbar {
    width: 0;  /* Remove scrollbar space */
    background: black;  /* Optional: just make scrollbar invisible */
}
/* Optional: show position indicator in red */
::-webkit-scrollbar-thumb {
    background: rgba(241, 43, 92,1);
}
</style>