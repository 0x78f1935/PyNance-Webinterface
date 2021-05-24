<template>
  <v-simple-table>
    <template v-slot:default>
        <thead>
            <tr>
                <th>Icon</th>
                <th>Description</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><v-icon large>mdi-menu</v-icon></td>
                <td>Opens the sidebar navigation menu</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-currency-usd</v-icon></td>
                <td>Indicates if PyNance is online and running, can be used to turn the bot on</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-currency-usd-off</v-icon></td>
                <td>Indicates if PyNance is offline and paused, can be used to turn the bot off</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-trademark</v-icon></td>
                <td>Configure your trade configuration for PyNance here</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-wallet</v-icon></td>
                <td>Provides statistics of your wallets available from Binance</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-chart-line</v-icon></td>
                <td>Gives you insights on bot statistics, provides an overview of what the bot is currently doing</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-github</v-icon></td>
                <td>Navigate to the source code of PyNance available on Github</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-discord</v-icon></td>
                <td>Join the official PyNance discord to stay up-to-date with the latest updates</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-lock</v-icon></td>
                <td>Lock your PyNance instance</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-cog</v-icon></td>
                <td>Configure PyNance, Add API keys or make backups!</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-help</v-icon></td>
                <td>This PyNance guide helps you setup your environment</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-backburger</v-icon></td>
                <td>Hides the sidebar navigation menu</td>
            </tr>
        </tbody>
    </template>
  </v-simple-table>
</template>

<script>
    export default {
        name: 'help-menu'
    }
</script>

<style lang="scss" scoped>

</style>