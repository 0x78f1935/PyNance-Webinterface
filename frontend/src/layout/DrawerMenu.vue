<template>
  <div>
    <v-navigation-drawer
      v-if="drawer"
      v-model="drawer"
      app
      class="pt-4"
      color="dark"
      mini-variant
    >
      <v-badge bottom overlap bordered color="green" v-if="this.$store.getters.online">
        <v-icon large>mdi-currency-usd</v-icon>
      </v-badge>
      <v-badge bottom overlap bordered color="red" v-else>
        <v-icon large>mdi-currency-usd-off</v-icon>
      </v-badge>

      <v-spacer class="mt-4"></v-spacer>

      <v-btn class="menu-btn" color="accent">
        <v-icon large v-if="this.$store.getters.online">mdi-currency-usd-off</v-icon>
        <v-icon large v-else>mdi-currency-usd</v-icon>
      </v-btn>
      <v-spacer class="mb-4"></v-spacer>

      <!-- <v-btn class="menu-btn" color="accent"><v-icon large>mdi-camera-metering-spot</v-icon></v-btn>
      <v-btn class="menu-btn" color="accent"><v-icon large>mdi-graph</v-icon></v-btn> -->
      <router-link to="/trades">
        <v-btn class="menu-btn" color="accent"><v-icon large>mdi-trademark</v-icon></v-btn>
      </router-link>

      <v-spacer class="mb-4"></v-spacer>
      <router-link to="/wallet">
        <v-btn class="menu-btn" color="accent"><v-icon large>mdi-wallet</v-icon></v-btn>
      </router-link>
      <router-link to="/statistics">
        <v-btn class="menu-btn" color="accent"><v-icon large>mdi-chart-line</v-icon></v-btn>
      </router-link>
      <router-link to="/news">
        <v-btn class="menu-btn" color="accent"><v-icon large>mdi-newspaper</v-icon></v-btn>
      </router-link>
      <v-spacer class="mb-4"></v-spacer>
      <v-btn class="menu-btn" color="accent" @click="window.open('https://github.com/0x78f1935/PyNance-Webinterface/tree/master', '_blank');"><v-icon large>mdi-github</v-icon></v-btn>
      <v-btn class="menu-btn" color="accent"><v-icon large>mdi-discord</v-icon></v-btn>
      <v-spacer class="mb-4"></v-spacer>
      <router-link to="/config">
        <v-btn class="menu-btn" color="accent"><v-icon large>mdi-cog</v-icon></v-btn>
      </router-link>
      <v-btn class="menu-btn" color="accent"><v-icon large>mdi-lock</v-icon></v-btn>
      <v-spacer class="mb-4"></v-spacer>
      <router-link to="/guide">
        <v-btn class="menu-btn" color="accent"><v-icon large>mdi-help</v-icon></v-btn>
      </router-link>
      <v-btn class="menu-btn" color="accent" @click="drawer = !drawer"><v-icon large>mdi-backburger</v-icon></v-btn>

    </v-navigation-drawer>
    <v-app-bar dense flat class="app-bar-thing">
      <v-btn @click="drawer = !drawer" class="menu-btn-open" color="accent" :disabled="drawer || !this.$store.getters.authenticated"><v-icon large>mdi-menu</v-icon></v-btn>
      <knightrider :txt="`PyNance - ${this.$router.currentRoute.name.toLowerCase()}`"></knightrider>
    </v-app-bar>
  </div>
</template>

<script>
import Knightrider from '../components/Knightrider.vue'
    export default {
        name: 'drawer-menu',
        components: {
          Knightrider,
        },
        data: () => ({
          drawer: false
        }),
    }
</script>

<style scoped>
.menu-btn, .menu-btn-open {
  margin: 2px;
  margin-bottom: 2px;
  width: 100%;
  max-width: 53px !important;
  min-width: 0 !important;
}

.menu-btn-open {
  height: 100%;
  min-height: 100%;
}
</style>

<style>
.app-bar-thing div, .v-toolbar__content, .v-toolbar__extension {
  padding: 0px !important;
}
</style>