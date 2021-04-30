<template>
    <v-card
        class="mx-auto custom_card"
        max-width="374"
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
                        <th class="title_custom">Type</th>
                        <th>Amount</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="title_custom">Available</td>
                        <td>{{ parseInt(free) + parseInt(locked) }}</td>
                    </tr>
                    <tr>
                        <td class="title_custom">Free</td>
                        <td>{{ free }}</td>
                    </tr>
                    <tr>
                        <td class="title_custom">Locked</td>
                        <td>{{ locked }}</td>
                    </tr>
                    <tr>
                        <td class="title_custom">Freezed</td>
                        <td>{{ freezed }}</td>
                    </tr>
                </tbody>
            </table>
        </v-card-text>

        <v-divider class="mx-4"></v-divider>

        <!-- <v-card-actions style="justify-content:space-between !important">
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
        </v-card-actions> -->
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
    }
</script>

<style lang="scss" scoped>
table, th, td {
    border: 1px solid black;
    width: 100%;
}

td {
    text-align: center;
}
th.title_custom, td.title_custom {
    text-align: left !important;
    padding-left: 5px !important;
}

.custom_card {
    padding: 8px !important;
}
</style>