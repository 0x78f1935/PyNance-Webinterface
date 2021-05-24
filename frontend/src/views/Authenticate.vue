<template>
  <help-menu></help-menu>
  
</template>

<script lang="ts">
  import Vue from 'vue'
  import HelpMenu from '../components/HelpComponents/Menu.vue'

  export default Vue.extend({
    name: 'Authenticate',

    components: {
      HelpMenu
    },
  })
</script>
