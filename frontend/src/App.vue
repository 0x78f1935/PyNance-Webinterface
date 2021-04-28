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

  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import SystemBar from './layout/SystemBar.vue';
import drawerMenu from './layout/DrawerMenu.vue';

export default Vue.extend({
  components: { 
    drawerMenu,
    SystemBar,
  },
  name: 'App',

  data: () => ({
  }),
});
</script>

