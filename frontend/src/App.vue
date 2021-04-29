<template>
  <v-app>
    <v-container class="mb-1">
      <system-bar></system-bar>
    </v-container>
    <drawer-menu></drawer-menu>

    <v-main>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-main>

    <v-footer app>
      Version: {{ $store.getters.version }}
    </v-footer>

    <first-time-setup v-if="!this.$store.getters.authentication"></first-time-setup>
    <login v-else></login>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import SystemBar from './layout/SystemBar.vue';
import drawerMenu from './layout/DrawerMenu.vue';
import FirstTimeSetup from './components/FirstTimeSetup.vue';
import Login from './components/Login.vue';

export default Vue.extend({
  components: { 
    drawerMenu,
    SystemBar,
    FirstTimeSetup,
    Login,
  },
  name: 'App',

  data: () => ({
  }),

  mounted () {
    this.$store.dispatch('loadDashboard');
  },
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