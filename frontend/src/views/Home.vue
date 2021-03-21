<template>
  <b-container fluid>
    <orderhistory></orderhistory>
  </b-container>
</template>

<script lang="ts">
  import Orderhistory from '@/components/orders.vue';
  export default {
    components: {
      Orderhistory,
    },
  }
</script>
