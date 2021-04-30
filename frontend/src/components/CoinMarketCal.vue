<template>
    <v-row>
        <v-col
            cols="4"
            class="mt-2"
        >
            <v-text-field
                :disabled="loading"
                v-model="search"
                label="Search for news item"
            >
                <v-icon
                    slot="prepend"
                    color="accent"
                >mdi-magnify
                </v-icon>
            </v-text-field>
        </v-col>

        <v-col
            class="mt-2"
            cols="4"
        >
            <v-slider
                :disabled="loading"
                v-model="max"
                label="Total items on page"
                :hint="max_items.toString()"
                color="accent"
                max="75"
                min="1"
                persistent-hint
                class="mr-2"
                step="1"
                thumb-label
            ></v-slider>

        </v-col>

        <v-col
            class="mt-2"
            cols="4"
            style="text-align: end"
        >
            <v-progress-circular
                v-if="loading"
                indeterminate
                color="accent"
                class="mr-2"
            ></v-progress-circular>
            <v-btn :disabled="page <= 1 || loading" @click="previousPage" class="mr-2">Previous Page</v-btn>
            <v-btn :disabled="page >= total_pages || loading" @click="nextPage" class="mr-2">Next Page</v-btn>
            <span class="mr-2">{{ page }} / {{ total_pages }}</span>
        </v-col>

        <v-col
            class="mt-2"
            cols="6"
        >
            <v-combobox
                solo
                :disabled="loading"
                label="Sort By"
                v-model="_sortBy"
                :items="sortByOptions"
                clearable
                hide-selected
            ></v-combobox>
        </v-col>
        <v-col
            class="mt-2"
            cols="6"
        >
            <v-combobox
                solo
                label="Show Only"
                v-model="_showOnly"
                :items="showOnlyOptions"
                :disabled="loading"
                clearable
                hide-selected
            ></v-combobox>
        </v-col>

        <v-col
            v-for="event, index in events"
            :key="index"
            :class="isCollapsed(event, search)"
            cols="6"
            md="2"
        >
            <v-card
                :loading="loading"
                class="mx-auto"
                max-width="374"
            >
            <template slot="progress">
                <v-progress-linear
                    color="accent"
                    height="10"
                    indeterminate
                ></v-progress-linear>
            </template>

                <v-card-text>
                    <div class="subtitle-1" v-for="coin, coin_index in event.coins" :key="`${index}_${coin_index}`">
                        {{ coin.fullname }}
                    </div>
                </v-card-text>

                <v-card-title>{{ event.title }}</v-card-title>

                <v-divider class="mx-4"></v-divider>

                <v-card-title style="font-size: 1rem !important">
                    {{ new Date(event.date_event).toLocaleDateString("en-US", { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}
                    <small v-if="event.can_occur_before">
                        &nbsp;(or earlier)
                    </small>
                </v-card-title>

                <v-card-text>
                    <v-chip-group
                        active-class="deep-purple accent-4 white--text"
                        column
                        v-if="event.categories"
                    >
                        <v-chip v-for="category, cat_index in event.categories" :key="`${index}_${cat_index}`">{{ category }}</v-chip>
                    </v-chip-group>
                </v-card-text>

                <v-card-actions style="justify-content:space-between !important">
                    <v-btn
                        color="accent lighten-2"
                        text
                        @click="goto(event.proof)"
                    >
                        Proof
                    </v-btn>
                    <v-btn
                        color="accent lighten-2"
                        text
                        @click="goto(event.source)"
                    >
                        Source
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-col>
    </v-row>
</template>

<script>
    import axios from 'axios'

    export default {
        name: 'coinmarketcal',
        data: () => ({
            loading: true,
            page: 1,
            max_items: 72,
            total_pages: 1,
            total_items: 0,
            events: [],
            sortBy: null,
            sortByOptions: ['created_desc', 'hot_events', 'trending_events', 'significant_events'],
            showOnly: null,
            showOnlyOptions: ['hot_events', 'trending_events', 'significant_events'],
            search: ''
        }),
        mounted () {
            this.fetchData();
        },
        computed: {
            max: {
                get() {return this.$data.max_items },
                set(value) {
                    this.$data.max_items = value;
                    this.fetchData();
                }
            },
            _sortBy: {
                get() {return this.$data.sortBy },
                set(value) {
                    this.$data.sortBy = value;
                    this.fetchData();
                }
            },
            _showOnly: {
                get() {return this.$data._showOnly },
                set(value) {
                    this.$data._showOnly = value;
                    this.fetchData();
                }
            },
        },
        methods: {
            isCollapsed(event, s) {
                console.log(event.title.toUpperCase().includes(s.toUpperCase()));
                if (event.coins.map(x => x.name).join('|').toString().toUpperCase().includes(s.toUpperCase()) ||
                    event.title.toUpperCase().includes(s.toUpperCase())
                ) {
                    return 'visible';
                }
                return 'collapse';
            },
            fetchData(){
                this.$data.loading = true;
                axios.post(`/api/v1/coinmarketcal/events`, {
                    'page': this.$data.page,
                    'max': this.$data.max_items,
                    'sortBy': this.$data.sortBy,
                    'showOnly': this.$data.showOnly
                }, {headers: {'token': this.$store.getters.token}}).then(response => {
                    console.log(response.data);
                    this.$data.total_pages = response.data.pagecount;
                    this.$data.total_items = response.data.total_items;
                    this.$data.events = response.data.events;
                    this.$data.loading = false;
                })

            },
            goto(url) {
                window.open(url, '_blank');
            },
            previousPage(){
                if (this.$data.page > 1){
                    this.$data.page -= 1;
                    this.fetchData();
                }
            },
            nextPage(){
                if (this.$data.page < this.$data.total_pages){
                    this.$data.page += 1;
                    this.fetchData();
                }
            },

        },
    }
</script>

<style lang="scss" scoped>

</style>