<template>
    <v-card
        class="mx-auto"
        max-width="374"
        :class="isVisible ? 'visible' : `hidden` "
    >
    <template slot="progress">
        <v-progress-linear
            color="accent"
            height="10"
            indeterminate
        ></v-progress-linear>
    </template>

        <v-card-title>{{ coinName }}</v-card-title>
        <v-card-text>
            <div class="subtitle-1">
                {{ projectName }}
            </div>
        </v-card-text>


        <v-divider class="mx-4"></v-divider>

        <v-card-text>
            <table>
                <thead>
                    <tr>
                        <td>Type</td>
                        <td>Amount</td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Available</td>
                        <td>{{ parseInt(free) + parseInt(locked) }}</td>
                    </tr>
                    <tr>
                        <td>Free</td>
                        <td>{{ free }}</td>
                    </tr>
                    <tr>
                        <td>Locked</td>
                        <td>{{ locked }}</td>
                    </tr>
                    <tr>
                        <td>Freezed</td>
                        <td>{{ freezed }}</td>
                    </tr>
                </tbody>
            </table>
        </v-card-text>

        <v-divider class="mx-4"></v-divider>

        <v-card-actions style="justify-content:space-between !important">
            <v-btn
                color="accent lighten-2"
                text
            >
                Test
            </v-btn>
            <v-btn
                color="accent lighten-2"
                text
            >
                Test
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script>
    export default {
        name: 'wallet-info',
        props: {
            coinName: {
                type: String,
                required: true
            },
            projectName: {
                type: String,
                required: true
            },
            free: {
                type: String,
                required: true
            },
            freezed: {
                type: String,
                required: true
            },
            locked: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                isVisible: true
            }
        },
        methods: {
            toggle(value) {
                this.$data.isVisible = value;
            },
        },
    }
</script>

<style lang="scss" scoped>
table, th, td {
    border: 1px solid black;
    width: 100%;
}
.hidden {
    display: none;
}
</style>