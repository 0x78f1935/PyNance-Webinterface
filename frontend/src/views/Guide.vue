<template>
    <v-container fluid>
        <v-card class="mx-auto">
            <v-tabs vertical color="accent">
                <v-tab class="taby">
                    <v-icon left>mdi-alert</v-icon>
                    Disclaimer
                </v-tab>
                <v-tab class="taby">
                    <v-icon left>mdi-snake</v-icon>
                    PyNance
                </v-tab>
                <v-tab class="taby">
                    <v-icon left>mdi-menu</v-icon>
                    Navigation
                </v-tab>
                <v-tab class="taby">
                    <v-icon left>mdi-api</v-icon>
                    Tokens
                </v-tab>
                <v-tab class="taby">
                    <v-icon left>mdi-currency-usd</v-icon>
                    PyNance Status
                </v-tab>
                <v-tab class="taby">
                    <v-icon left>mdi-trademark</v-icon>
                    PyNance Config
                </v-tab>
                <v-tab class="taby">
                    <v-icon left>mdi-chart-line</v-icon>
                    Trade Statistics
                </v-tab>
                <v-tab class="taby">
                    <v-icon left>mdi-heart-half-full</v-icon>
                    Show some love
                </v-tab>

                <v-tab-item>
                    <v-card flat>

                        <v-img height="375" src="../assets/stonks/terror.gif"></v-img>

                        <v-card-title>Disclaimer</v-card-title>

                        <v-card-text>
                            <p>
                                This tool is not a money printing tool and contains risks. <br>
                                You are responsible for your own money and actions.
                            </p>

                            <p>
                                By using this tool you agree to take FULL responsibility for your own money. <br>
                                Even if this would mean missed opportunities caused by the algorithm of this bot or worse; losses. <br>
                                Be responsible, Only trade with money you can afford to lose.
                            </p>

                            <p class="mb-0">
                                Make sure to read through this guide before going online and start trading with PyNance. <br>
                                A wrong configuration can lead to bankruptcy. If you are a beginner it's strongly recommended to begin with SPOT trading. <br>
                                SPOT Trading is the most safest option within PyNance. <br>
                                Use future trading only if you can handle losses and if you know what you are doing.
                            </p>

                        </v-card-text>
                    </v-card>
                </v-tab-item>

                <v-tab-item>
                    <v-card flat>
                        <v-card-title>PyNance - About</v-card-title>
                        <v-card-text>
                            <p>
                                PyNance is created to automate crypto trading on Binance. <br>
                                The project PyNance exists out of two different projects; PyNance-<strong>core</strong> and the PyNance-<strong>webinterface</strong>. <br>
                                The webinterface is build on-top of the core library. The core library could be used as standalone.<br>
                                The webinterface however is unable to operate without the core library.
                            </p>
                        </v-card-text>
                        <v-card-title>PyNance - Core</v-card-title>
                        <v-card-text>
                            <p>
                                There are a few Binance python libraries out there, but since the crypto space is full of scammers it was suspicious to me.<br>
                                Once going down the rabbit hole I found some weird dependencies. <br>
                                Therefor I had decided to make my own opensource Binance API library. <br>
                            </p>
                            <p class="mb-0">
                                Reinventing the wheel comes with a downside. Not all availabe Binance endpoints are available in PyNance-Core. <br>
                                Only endpoints that the webinterface-listener needs in order to operate automated buy and sell orders. <br>
                                <strike>Yes, There is also a listener but it comes with the webinterface since version 3.0.0</strike>
                            </p>
                        </v-card-text>
                        <v-card-title>PyNance - Webinterface</v-card-title>
                        <v-card-text>
                            <p>
                                PyNance webinterface is developed to put core logic into a UI interface to keep things simple and interesting. <br>
                                So why a webinterface? A webinterface provides a lot of adventage if you are in your own network. <br>
                                You could visit your webserver from your smartphone while have it open on your laptop! <br>
                            </p>
                            <p class="mb-0">
                                Unless making changes to your network your PyNance instance will only work inside your own network. <br>
                                This means it will not be accessible from the internet, the master password is inplace to protect you from your own kids visiting localhost ports... ;)
                            </p>
                        </v-card-text>
                        <v-card-title>So Why sould I trust PyNance?</v-card-title>
                        <v-card-text>
                            <p>
                                PyNance is 100% opensource and has no weird dependencies. <br>
                                PyNance-Core only makes use of the Python library <strong>requests</strong> in order to talk with the Binance API server. <br>
                            </p>
                            <p>
                                The webinterface itself is also 100% opensource and is based on the Python library <strong>Flask</strong>.<br>
                                Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.<br>
                                It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions.<br>
                            </p>
                            <p class="mb-0">
                                The goal for Flask is to extend the webserver with what PyNance needs. The requirements of the webinterface can be found on github. <br>
                                So, can i trust PyNance? Well, long story short.. that is all up to you!
                            </p>
                        </v-card-text>
                    </v-card>
                </v-tab-item>

                <v-tab-item>
                    <v-card flat>
                        <v-card-title>Navigation</v-card-title>
                        <v-card-text>
                            <p>
                                By reading this we can assume that you now know how to open the sidebar.<br>
                                The sidebar allows you to navigate through the PyNance Webinterface. <br>
                                Some icons in the sidebar might be obvious and some might raise questions. <br>
                                Therefor we have prepared a table which gives you an overview over all those icons.
                            </p>
                            <p class="mb-0">
                                <help-menu></help-menu>
                            </p>
                        </v-card-text>
                    </v-card>
                </v-tab-item>

                <v-tab-item>
                    <v-card flat>
                        <v-card-title>Binance API credentials</v-card-title>
                        <v-card-text>
                            <p>
                                The Binance API Credentials are required in order to use PyNance. <br>
                                When those credentials are invalid or not provided PyNance will simply not work.
                            </p>
                            <p>
                                Remember that token you placed in <strong>.env.production</strong>? I hope you did. <br>
                                If you don't I strongly recommend to close pynance webinterface and reinstall it. (refer to the readme.md file) <br>
                                If you did, Congrats!,. Assuming you have entered the correct Binance API credentials you can restrict your API if you like. <br>
                                PyNance needs atleast 3 restrictions. Open Binance and go to the API Management tab.
                            </p>

                            <ul>
                                <li>Enable Reading</li>
                                <li>Enable Spot & Margin Trading</li>
                                <li>Enable Futures</li>
                            </ul>

                            <p class="mb-0">
                                You can also restrict access to only allow making request from any IP you put into the <strong>Restrict access to trusted IPs only (Recommended)</strong> field.<br>
                                A google search <code>what is my ip</code> can help you out with what your IP is to fill in.
                            </p>

                        </v-card-text>

                        <v-card-title>General <v-icon large>mdi-api</v-icon> information</v-card-title>

                        <v-card-text>
                            <p class="mb-0">
                                API-Keys / tokens other then the Binance API-Key and API-Secret can be configured in the <v-icon small>mdi-cog</v-icon> configuration page. <br>
                                The <v-icon small>mdi-cog</v-icon> configuration page can be located in the sidebar menu. <br>
                                Once you saved a new API-Key on this page make sure to refresh the page once to make sure all the endpoints get a chance to pick up on the newly provided data.
                            </p>
                        </v-card-text>

                        <v-card-title>CoinMarketCal API-key</v-card-title>
                        <v-card-text>
                            <p>
                                coinmarketcal.com is a trusty source of relevant crypto news. It is always on point. <br>
                                One of the goals for PyNance is to keep things simple for users who are not into coding but still want to have a working bot. <br>
                                Therefor it is not required to have a coinmarketcal api-key in order to make use of PyNance. <br>
                                If you however decide to create a coinmarketcal.com account to obtain an API key you will be able to check coinmarketcal within PyNance webinterface.
                            </p>
                            <p>
                                Obtaining an API-key is free. In order to obtain an API-key
                            </p>

                            <ul>
                                <li>Go to https://coinmarketcal.com/en/developer/login</li>
                                <li>Create a new account if you don't have an account yet and login</li>
                                <li>Copy the api-key from your dashboard and save it in the PyNance configuration <v-icon small>mdi-cog</v-icon> page</li>
                            </ul>

                            <p class="mb-0">
                                You can change this API-key on the fly anytime you want on the PyNance configuration <v-icon small>mdi-cog</v-icon> page. <br>
                                This has no direct impact on the bot itself.
                            </p>

                        </v-card-text>
                    </v-card>
                </v-tab-item>

                <v-tab-item>
                    <v-card flat>
                        <v-card-title>Online Status <v-icon large>mdi-currency-usd</v-icon></v-card-title>
                        <v-card-text>
                            <p>
                                The sidebar menu provides in the top corner an icon which indicates if the bot is running or not. <br>

                                <v-badge bottom overlap bordered color="green">
                                    <v-icon large>mdi-currency-usd</v-icon>
                                </v-badge> with a green dot indicates that the bot is online and looking for trades. <br>
                                <v-badge bottom overlap bordered color="red">
                                    <v-icon large>mdi-currency-usd-off</v-icon>
                                </v-badge>with a red dot indicates that the bot is offline.                                
                            </p>

                            <p class="mb-0">
                                The icon appears also in the sidebar menu as a button. When used it toggles PyNance off and online.
                            </p>
                        </v-card-text>

                        <v-card-title>Statusbar</v-card-title>
                        <v-card-text>
                            <p class="mb-0">
                                The statusbar is the blackbar bar top of you screen. When running PyNance for the first time it will indicate an offline message.<br>
                                Once the bot is taking orders and scanning for relevant prices or switching between symbols all that info comes back to the statusbar. <br>
                                Its a very nice little way to see on each page on the webinterface what PyNance is currently doing. 
                            </p>
                        </v-card-text>
                    </v-card>
                </v-tab-item>
                    
                <v-tab-item>
                    <v-card flat>
                        <v-card-title>PyNance Configuration</v-card-title>
                        <v-card-text>
                            <p>
                                PyNance can be configured to your likings. This is also the risky part of trading. But once set, your good to go!<br>
                                To open the trade configuration simply click the <v-icon large>mdi-trademark</v-icon> icon in the sidebar menu. <br>
                                There are alot of parameters which can be configured. This page is also used to switch between SPOT and future trading.
                            </p>

                            <p>
                                SPOT trading is enabled by default. You cannot run SPOT and future trading at the same time. <br>
                                In order to switch you have to disable the <code>Trading in Spot!</code> button.
                            </p>

                            <p>
                                There is also an option called <strong>sandbox</strong>. When enabled PyNance would run like normal but would not place any order.<br>
                                This option allows you to test your configuration before you try it for real.
                            </p>

                            <p class="mb-0">
                                Each parameter that can be configured on this page is different for SPOT and for future trading other then <code>Symbols</code>. <br>
                                Symbols is used to select the "symbols" you would like to trade. For example <strong>LTCUSDT</strong> or <strong>ADAUSDT</strong>. <br>
                                You can use multiple symbols but keep in mind that too many symbols might result in an API-Key ban from Binance. <br>
                                Just don't be greedy. PyNance has been tested with 10 symbols at the same time and could easily handle 20 at the same time.
                            </p>
                        </v-card-text>
                        <v-card-title>SPOT Trading</v-card-title>
                        <v-card-text>
                            <p>
                                SPOT Trading is relative safe. The stratagy behind SPOT trading is simple.
                            </p>
                            <ul>
                                <li>Get buy entry based on (lowest average - suppression)</li>
                                <li>Waits until buy entry requirements met</li>
                                <li>Holds until Sell entry requirements met</li>
                                <li>Sell entry when price meets expected profit margin</li>
                                <li>Repeat</li>
                            </ul>
                        </v-card-text>
                        <v-card-title>Future Trading</v-card-title>
                        <v-card-text>
                            <p>
                                Future trading brings risks to the table but a higher reward. <br>
                                The bot will trade small longs and shorts based on the configuration provided. <br>
                            </p>
                            <p>
                                Future is still under development #TODO
                            </p>
                            <ul>
                                <li></li>
                                <li></li>
                                <li></li>
                                <li></li>
                            </ul>
                        </v-card-text>

                        <v-card-title>Current Prices</v-card-title>
                        <img src="@/assets/prices.png"/>
                        <v-card-text>
                            <p class="mb-0">
                                Current prices can be seen when configuring PyNance.<br>
                                You can use the search bar to filter out unwanted symbols. <br>
                                Use the quantity input to change the <code>cost(s)</code> of a symbol.<br>
                                If we look at <code>ADABTC</code>, <code>1</code> <strong>ADA</strong> is <code>0.00003506</code> <strong>BTC</strong> worth.<br>
                                If you would buy <code>120</code><strong>ADA</strong> you would need <code>0.0042072000</code><strong>BTC</strong>.
                            </p>
                        </v-card-text>

                        <v-card-title>Additional information</v-card-title>
                        <v-card-text>
                            <p class="mb-0">
                                You can still trade within binance manually when running the bot. <br>
                                Please do keep in mind when trading SPOT the bot will move funds around. <br>
                                Once you accidentally sell bot holdings the bot will notice and put its own order on hold. <br>
                                After it will continue with what it was doing.
                            </p>
                        </v-card-text>
                    </v-card>
                </v-tab-item>            

                <v-tab-item>
                    <v-card flat>
                        <v-card-title>PyNance Statistics</v-card-title>
                        <v-card-text>
                            <p>
                                This might be the most interesting page to look at. <br>
                                Once PyNance is running with a valid configuration you will see the target symbols price in the graph available on the <v-icon small>mdi-chart-line</v-icon> Statistics page. <br>
                                If you are running PyNance on a smaller screen there will be no graph. <br>
                                To the right of the graph you can find the legend of the graph but also additional information on the symbol PyNance is processing at that moment. <br>
                                The data which is being processed is rendered into the graph to give a better representation on what the bot is doing and looking at. <br>
                                Based on this information you can change your bot stratagy accordingly. 
                            </p>

                            <p>
                                The table below the graph shows the order history of PyNance. All the orders placed by PyNance can be found here. <br>
                                Each value has its own meaning.
                            </p>

                            <v-simple-table>
                                <template v-slot:default>
                                    <thead>
                                        <tr>
                                            <th>Table Column</th>
                                            <th>Description</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td>Active</td>
                                            <td>Indicates if this is the current order is currently being processed by PyNance</td>
                                        </tr>
                                        <tr>
                                            <td>Brought Price</td>
                                            <td>Shows 0 if nothing has been brought yet, otherwise it shows the price it costed to buy this order</td>
                                        </tr>
                                        <tr>
                                            <td>Created</td>
                                            <td>Shows the date of this symbol of when this symbol got processed for the first time by PyNance</td>
                                        </tr>
                                        <tr>
                                            <td>Quantity</td>
                                            <td>Shows 0 if nothing has been brought yet, otherwise it shows the total amount of the symbol brought by PyNance.</td>
                                        </tr>
                                        <tr>
                                            <td>Sold For</td>
                                            <td>Shows 0 if nothing has been sold yet, Otherwise it shows the price which PyNance sold the order for.</td>
                                        </tr>
                                        <tr>
                                            <td>Spot</td>
                                            <td>True if this order is a SPOT order, otherwise False</td>
                                        </tr>
                                        <tr>
                                            <td>Symbol</td>
                                            <td>The symbol which is used in this order</td>
                                        </tr>
                                        <tr>
                                            <td>Updated</td>
                                            <td>The date the order got updated for for the last time</td>
                                        </tr>
                                    </tbody>
                                </template>
                            </v-simple-table>

                            <p class="mb-0">
                                Hopefully the information provided on this page provides you with more insights on the performance of the bot and overtime perhaps more profit.
                            </p>
                        </v-card-text>
                    </v-card>
                </v-tab-item>

                <v-tab-item>
                    <v-card flat>
                        <v-card-title>Show some love!</v-card-title>
                        <v-card-text>
                            <p class="mb-0">
                                PyNance took a lot of work to get it where it is now.<br>
                                If you like my work there are a few things you could do to draw my attention.
                            </p>
                        </v-card-text>

                        <v-card-title>Join the PyNance <v-icon large>mdi-discord</v-icon> community!</v-card-title>
                        <v-card-text>
                            <p class="mb-0">
                                You can join the PyNance <v-icon small>mdi-discord</v-icon> community through the sidebar menu.<br>
                                Feel free to leave suggestions, report bugs or have just a good time with other people with the same interests.<br>
                                Once joined you will be eligible for competitions time from time mostly funded by you guys.<br>
                                If that is not enough you also will be able to stay up-to-date with the latest PyNance versions / news.
                            </p>
                        </v-card-text>

                        <v-card-title>Leave a <v-icon large>mdi-star</v-icon> on Github</v-card-title>
                        <v-card-text>
                            <p class="mb-0">
                                Another thing you could do is simply navigate to the source-code of PyNance and leave a star. <br>
                                The sidebar menu has a <v-icon small>mdi-github</v-icon> Github button which redirects you to the source-code.
                            </p>
                        </v-card-text>

                        <v-card-title>Or simply donate</v-card-title>
                        <v-card-text>
                            <p>
                                By donating you allow the PyNance community to grow. As stated earlier competitions will take place from now and then in the discord community.<br>
                                Donating also allows me to dedicate more time into the development for PyNance. It is not required however to donate in order to make full use of PyNance. <br>
                                PyNance is free, open-source, "decentralized" and fully community driven and its ment that way.
                            </p>
                            <p class="mb-0">
                                BTC Address <code>1HpywjQRi5jmpYxZXo32VAgVmyHZLacbJG</code>
                            </p>

                        </v-card-text>
                    </v-card>
                </v-tab-item>
            </v-tabs>
        </v-card>
    </v-container>
</template>

<script>
    import HelpMenu from '../components/HelpComponents/Menu.vue'
    export default {
        components: {
            HelpMenu,
        },
        data() {
            return {
                currentTab: 0
            }
        },
    }
</script>

<style lang="css" scoped>
    .taby{
        min-width: 210px;
        justify-content: space-between;
    }
</style>