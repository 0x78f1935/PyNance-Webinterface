<template>
  <b-container fluid>
    <b-row>
      <candle-graph></candle-graph>
    </b-row>
    <b-row>
      <b-col class="col-md-4">
        <spark-graph :updateCandles="true" evaluate="close" :card="true"></spark-graph>
      </b-col>
      <b-col class="col-md-4">
        <spark-graph evaluate="high" :card="true"></spark-graph>
      </b-col>
      <b-col class="col-md-4">
        <spark-graph evaluate="ignore" :card="true"></spark-graph>
      </b-col>
      <b-col class="col-md-4">
        <spark-graph evaluate="low" :card="true"></spark-graph>
      </b-col>
      <b-col class="col-md-4">
        <spark-graph evaluate="open" :card="true"></spark-graph>
      </b-col>
      <b-col class="col-md-4">
        <spark-graph evaluate="quote_volume" :card="true"></spark-graph>
      </b-col>
      <b-col class="col-md-4">
        <spark-graph evaluate="taker_buy_base" :card="true"></spark-graph>
      </b-col>
      <b-col class="col-md-4">
        <spark-graph evaluate="taker_buy_quote" :card="true"></spark-graph>
      </b-col>
      <b-col class="col-md-4">
        <spark-graph evaluate="trades" :card="true"></spark-graph>
      </b-col>
    </b-row>

  </b-container>
</template>

<script>
// @ is an alias to /src
import SparkGraph from '@/components/SparkGraph.vue';
import CandleGraph from '@/components/CandleGraph.vue';

export default {
  name: 'Home',
  components: {
    SparkGraph,
    CandleGraph
  },
  beforeCreate(){
    this.$store.dispatch('get_candlesticks');
  },
  created () {
    setInterval(
        () => { this.$store.dispatch('get_candlesticks') },
        1000
    )
  },
}
</script>