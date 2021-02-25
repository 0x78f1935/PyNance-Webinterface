<template>
    <div v-if="simplified == true">
        <b-row>
            <span class="right"><small class="text-s">{{balance_1.asset}} {{ parseFloat(balance_1.value).toFixed(8) }}</small></span>
        </b-row>
        <b-row>
            <span class="right"><small class="text-s">{{balance_2.asset}} {{ parseFloat(balance_2.value).toFixed(8) }}</small></span>
        </b-row>
    </div>
    <div v-else style="min-width: 100%">
        <b-row>
            <b-col>
                <b-row>
                    <span class="right"><small class="text-s">{{balance_1.asset}} {{ parseFloat(balance_1.value).toFixed(8) }}</small></span>
                </b-row>
                <b-row>
                    <span class="right"><small class="text-s">{{balance_2.asset}} {{ parseFloat(balance_2.value).toFixed(8) }}</small></span>
                </b-row>
            </b-col>
            <b-col>
                <b-row>
                    <span class="right"><small class="text-s">{{balance_1.asset}}-Free {{ parseFloat(balance_1.free).toFixed(8) }}</small></span>
                </b-row>
                <b-row>
                    <span class="right"><small class="text-s">{{balance_2.asset}}-Free {{ parseFloat(balance_2.free).toFixed(8) }}</small></span>
                </b-row>
            </b-col>
            <b-col>
                <b-row>
                    <span class="right"><small class="text-s">{{balance_1.asset}}-Locked {{ parseFloat(balance_1.locked).toFixed(8) }}</small></span>
                </b-row>
                <b-row>
                    <span class="right"><small class="text-s">{{balance_2.asset}}-Locked {{ parseFloat(balance_2.locked).toFixed(8) }}</small></span>
                </b-row>
            </b-col>
        </b-row>
    </div>
</template>

<script>
    import { price } from '@/components/utils';

    export default {
        name: 'balance',
        props: {
            simplified: {
                type: Boolean,
                default: false
            },
        },
        methods: {
            format_price(amount) {
                return price(amount, this.$store.getters.metrics);
            }
        },
        computed: {
            balance_1() { return this.$store.getters.total_balance_1; },
            balance_2() { return this.$store.getters.total_balance_2; },
        },
    }
</script>

<style scoped>
    .right{
        text-align:right;
        width: 100%;
        height: fit-content;
    }

    .text-m, .text-s {
        margin: 0px;
        padding: 0%;
    }

    .text-m{
        font-size: 80%;
    }

    .text-s{
        font-size: 70%;
    }

</style>