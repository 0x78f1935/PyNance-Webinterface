<template>
  <v-app>
    <nav-drawer></nav-drawer>

    <nav-header></nav-header>

    <!-- Sizes your content based upon application components -->
    <v-main>

      <!-- Provides the application the proper gutter -->
      <v-container fluid>

        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <global-footer></global-footer>
  </v-app>
</template>

<script>
import navDrawer from '@/components/NavigationDrawer';
import navHeader from '@/components/NavigationHeader';
import GlobalFooter from '@/components/GlobalFooter';

export default {
  name: 'App',
  components: {
    navDrawer,
    navHeader,
    GlobalFooter
  },
  created() {
    this.$vuetify.theme.dark = this.$store.getters.darkmode;
  },
};
</script>

<style>
html{
  overflow-y: hidden;
}
</style>