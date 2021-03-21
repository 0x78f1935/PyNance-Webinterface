<template>
    <v-app-bar app>
        <v-app-bar-nav-icon @click.stop="$store.dispatch('toggleDrawer', !$store.getters.drawer);"></v-app-bar-nav-icon>

        <v-toolbar-title class="p-0">{{ $t('Profit') }} <span :style="`color:${$store.getters.profitColor};`">{{ $store.getters.profit }}</span> {{ $store.getters.selectedProfit }}</v-toolbar-title>

        <b-col class="mr-auro small_average">
            <buyin></buyin>
        </b-col>

        <b-col class="mr-auto d-none d-md-block" cols="0" md="0">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-icon v-bind="attrs" v-on="on" v-if="$store.getters.online==true" size="25" class="image_max_size">mdi-signal</v-icon>
                    <v-icon v-bind="attrs" v-on="on" v-else-if="$store.getters.online==false" size="25" class="image_max_size">mdi-signal-off</v-icon>
                </template>
                <span><small>{{ $t('tooltipOnline') }}</small></span>
            </v-tooltip>
            &nbsp;
            <span class="label_centered" :style="$store.getters.online ? 'color:#4CAF50;' : 'color:#ff4081;'">{{ $store.getters.online ? 'Online' : 'Offline'}}</span>
        </b-col>
    </v-app-bar>
</template>

<script>
    import Buyin from '@/components/buyin.vue';

    export default {
        name:'nav-header',
        components: {
            Buyin,
        },
    }
</script>

<style lang="scss" scoped>
    .small_average {
        font-size: 12px;
        min-width: 150px;
    }
</style>