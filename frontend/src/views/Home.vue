<template>
  <b-container fluid>
    <b-row>
      <b-col class="col-md-4">
        <candle-graph :updateCandles="true" evaluate="close" :card="true"></candle-graph>
      </b-col>
      <b-col class="col-md-4">
        <candle-graph evaluate="high" :card="true"></candle-graph>
      </b-col>
      <b-col class="col-md-4">
        <candle-graph evaluate="ignore" :card="true"></candle-graph>
      </b-col>
      <b-col class="col-md-4">
        <candle-graph evaluate="low" :card="true"></candle-graph>
      </b-col>
      <b-col class="col-md-4">
        <candle-graph evaluate="open" :card="true"></candle-graph>
      </b-col>
      <b-col class="col-md-4">
        <candle-graph evaluate="quote_volume" :card="true"></candle-graph>
      </b-col>
      <b-col class="col-md-4">
        <candle-graph evaluate="taker_buy_base" :card="true"></candle-graph>
      </b-col>
      <b-col class="col-md-4">
        <candle-graph evaluate="taker_buy_quote" :card="true"></candle-graph>
      </b-col>
      <b-col class="col-md-4">
        <candle-graph evaluate="trades" :card="true"></candle-graph>
      </b-col>
    </b-row>

  </b-container>
</template>

<script>
// @ is an alias to /src
import CandleGraph from '@/components/CandleGraph.vue';

export default {
  name: 'Home',
  components: {
    CandleGraph
  },
  created () {
    setInterval(
        () => { this.$store.dispatch('get_candlesticks') },
        1000
    )
  },
}
</script>