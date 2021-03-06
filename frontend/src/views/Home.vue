<template>
  <b-container fluid>
    <b-row>
      <knightrider></knightrider>
    </b-row>
    <v-divider class="mt-3"></v-divider>
    <b-row>
      <current-fiat-coin-price></current-fiat-coin-price>
    </b-row>
    <b-row>
      <order-history style="margin-top: 15px"></order-history>
    </b-row>
  </b-container>
</template>

<script>
// @ is an alias to /src
// import CandleGraph from '@/components/CandleGraph.vue';
import OrderHistory from '@/components/OrderHistory.vue';
import Knightrider from '@/components/KnightRider.vue';
import CurrentFiatCoinPrice from '@/components/CurrentFiatCoinValue.vue';

export default {
  name: 'Home',
  components: {
    OrderHistory,
    Knightrider,
    CurrentFiatCoinPrice
  },
}
</script>