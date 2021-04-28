<template>
    <table>
        <thead>
            <tr>
                <td>Icon</td>
                <td>Description</td>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><v-icon large>mdi-menu</v-icon></td>
                <td>Opens the navigation menu</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-currency-usd</v-icon></td>
                <td>Indicates that PyNance is online and working, can be used to turn the bot on</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-currency-usd-off</v-icon></td>
                <td>Indicates that PyNance is offline and sleeping, can be used to turn the bot off</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-trademark</v-icon></td>
                <td>Configure your trade configuration</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-wallet</v-icon></td>
                <td>Provides statistics of your wallets</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-chart-line</v-icon></td>
                <td>Gives you insights on bot statistics</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-github</v-icon></td>
                <td>Navigate to the source code of PyNance</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-discord</v-icon></td>
                <td>Join the official PyNance discord</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-lock</v-icon></td>
                <td>Lock your PyNance instance</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-cog</v-icon></td>
                <td>Configure PyNance</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-help</v-icon></td>
                <td>This PyNance guide helps you to setup your environment</td>
            </tr>
            <tr>
                <td><v-icon large>mdi-backburger</v-icon></td>
                <td>Hides the navigation menu</td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    export default {
        name: 'help-menu'
    }
</script>

<style lang="scss" scoped>

</style>