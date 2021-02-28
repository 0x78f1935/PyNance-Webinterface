<template>
  <b-container fluid>
    <knightrider></knightrider>
    <order-history style="margin-top: 15px"></order-history>
  </b-container>
</template>

<script>
// @ is an alias to /src
// import CandleGraph from '@/components/CandleGraph.vue';
import OrderHistory from '@/components/OrderHistory.vue';
import Knightrider from '@/components/KnightRider.vue';

export default {
  name: 'Home',
  components: {
    OrderHistory,
    Knightrider,
  },
}
</script>