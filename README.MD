<span style="font-family:Papyrus; font-size:4em;"> PyNance </span>
<hr>
<a name="Disclaimer"></a><span style="font-family:Papyrus; font-size:3em;color:red;">DISCLAIMER</span><br/>
<span style="font-family:Papyrus; font-size:2.5em;color:red;"> This tool is not a money printing tool and contains risks. </span><br/>
You </strong> are <strong> responsible</strong> for <strong>your own money and actions.</strong> <br/><br/><strong>By using this tool you agree to take FULL responsibility of your own money. </strong><br/> Even if this would mean missed opportunities caused by the algorithm of this bot or worse; <strong style="color:red;">losses</strong>. <br/><br/><strong style="color:green;">Be responsible</strong>, Only trade with money you can afford to lose.<br/>Take chances, Make mistakes, Get messy.... To the moon! <br/><br/><hr/>

<span style="font-family:Papyrus; font-size:3em;color:red;">IMPORTANT NOTICE</span><br/>

This tool makes use of docker. Once a running container has been established and the port of your machine is public. everyone in the same network will be able to connect to PyNance. <span style="color:red;">The current version of PyNance has no login screen.</span> You can secure yourself if you host PyNance on the machine you would like to check the interface on. Just make sure to block the port PyNance is running on.<br/><br/>Please do note; When creating your API key you should only allow it to work if the traffic send to Binance is comming from your IP address. This does <strong style="color:orange;">not</strong> fix the problem described above.<hr>

# <a name="table-of-contents"></a>Table of Contents
1. [Table of Contents](#table-of-contents)
2. [Disclaimer](#Disclaimer)
3. [Why PyNance](#why)
4. [Requirements & Dependencies](#req)
    1. [Production Req and Dep](#req-prod)
    2. [Development Req and Dep](#req-dev)
5. [Get Started](#get-started)
    1. [Binance Account](#binance-account)
    2. [Binance API Credentials](#binance-api)
    3. [PyNance Configuration](#pynance-config)
    4. [PyNance Installation](#pynance-installation)
0. [Frequently Asked Questions](#faq)
0. [Community](#community)

# <a name="why"></a>Why PyNance

Binance is a crypto exchange which allows you to trade crypto currency. I got tired of looking at graphs all day to manage my stop limits so naturally I tried to figure out ways to automate this process. I found a couple of Python libraries which talked to the Binance api. The required dependencies looked a little weird to me so I decided to make my own Binance library. This library only has one dependency: `requests`. After playing around with it I created the very first PyNance bot based on this library. Some friends got interested but didn't knew how to code. I took this as one of my weekend projects which I usually schedule to not get bored and created this complete webinterface around it. The goal of PyNance is to swingtrade crypto currency. Create buy orders when the price is low, and sells when the price is high. This bot is more patient than you do!

# <a name="req"></a>Requirements & Dependencies

## <a name="req"></a>Production requirements & dependencies

You basically can run PyNance anywhere where docker is installed. If you don't have docker installed yet make sure to install the [latest version](https://www.docker.com/get-started). Once docker is installed you are all set. The only thing left to do is to configure PyNance so it will accept your API credentials. You can read more on that topic in [Get Started](#get-started).


## <a name="req"></a>Development requirements & dependencies

### nvm
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam commodo massa quis sem euismod convallis. Pellentesque ullamcorper sapien vitae nibh vulputate tincidunt. Aliquam nec diam ultrices, vehicula velit eu, dapibus turpis. Donec consectetur enim arcu, non rhoncus tellus imperdiet a. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Duis egestas felis id nisl gravida, vitae convallis dui tempor. Quisque eleifend erat eu tortor porttitor semper id ac urna. Cras quis molestie eros, nec consectetur turpis. Fusce interdum convallis ipsum semper porta. Sed dictum nisi at quam pulvinar vehicula. Quisque luctus, risus ut luctus egestas, diam purus laoreet lectus, non porttitor magna lacus ac tortor.

### node
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam commodo massa quis sem euismod convallis. Pellentesque ullamcorper sapien vitae nibh vulputate tincidunt. Aliquam nec diam ultrices, vehicula velit eu, dapibus turpis. Donec consectetur enim arcu, non rhoncus tellus imperdiet a. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Duis egestas felis id nisl gravida, vitae convallis dui tempor. Quisque eleifend erat eu tortor porttitor semper id ac urna. Cras quis molestie eros, nec consectetur turpis. Fusce interdum convallis ipsum semper porta. Sed dictum nisi at quam pulvinar vehicula. Quisque luctus, risus ut luctus egestas, diam purus laoreet lectus, non porttitor magna lacus ac tortor.

### python
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam commodo massa quis sem euismod convallis. Pellentesque ullamcorper sapien vitae nibh vulputate tincidunt. Aliquam nec diam ultrices, vehicula velit eu, dapibus turpis. Donec consectetur enim arcu, non rhoncus tellus imperdiet a. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Duis egestas felis id nisl gravida, vitae convallis dui tempor. Quisque eleifend erat eu tortor porttitor semper id ac urna. Cras quis molestie eros, nec consectetur turpis. Fusce interdum convallis ipsum semper porta. Sed dictum nisi at quam pulvinar vehicula. Quisque luctus, risus ut luctus egestas, diam purus laoreet lectus, non porttitor magna lacus ac tortor.

# <a name="get-started"></a>Get Started

Before we get started with PyNance I think its a good idea to explain the fundamentals of this bot. Once PyNance is installed you will be able to sellect two different kinds of currencies. **currency_1** and **currency_2**. PyNance will glue those two currencies together to form a `symbol`.
A symbol can look like `ADABUSD` or like `BTCUSDT`. Lets say we pick `BTCUSDT` that would mean, in order to start PyNance <span style="color:red">we need an available BTC balance in your spot wallet to be able to trade.</span> Once PyNance is online, it will look if the current value of ***in our case BTCUSDT*** is lower then the average price. If this is the case PyNance will buy (100% - minimal profit %) calculated over <span style="colr:red">the current amount available in your spot wallet</span>. This is the amount PyNance places a buy entry for. If PyNance was able to successfully bought some crypto it will switch its state to sale and starts selling the crypto. PyNance is patient and will hold the amount bought until the price is met, which is calculated based on the minimal profit percentage. <span style="color:green;">Profit is calculated excluding fees.</span> Fees are calculated in the buy-in price. If you like to FOMO for some weird reason but your funds are locked away because PyNance is running,.. No worry. PyNance got you covered. There is a "Panik" button, Once active PyNance will try to sell its crypto off without looking at profit. However It only sells when the current price is higher then the (bought-in price + costs of the fee). This way you can FOMO a little bit more secure without to much loss. Once Panik is active PyNance halts the procedure to buy new coins. When PyNance is selling it will sell all the balance which is available. In this example that would be all the `USDT` available. Then the cycle continues!

## <a name="binance-account"></a>Binance Account

In order to fetch the latest market information and to be able to place orders you will need a Binance account. [You can create an account here](https://www.binance.com/en/register?ref=73051759). This account also contains your wallets and API credentials. Make sure to enable 2factor authentication.

## <a name="binance-api"></a>Binance API Credentials

After you have created your [binance account](#binance-account) you need to create your API credentials. Once created make sure to save them. The secret is hidden after creation and you need the secret in order to proceed. [You can follow the steps on how to create API credentials here](https://www.binance.com/en/support/faq/360002502072-How-to-create-API).

## <a name="pynance-config"></a>PyNance Configuration

There are two environments available to you. `production` and `development`. Both environments work the exact same way. The main difference is that `production` should be used in the `docker environment`.

Navigate to the following path `/pynance-webinterface/backend/config`. \
In this location you should have atleast two files. `development.py` and `production.py` which represents those environments. `BINANCE_API_KEY` and `BINANCE_API_SECRET` are the two values which should contain your API credentials obtained from [Binance](#binance-api).

<span style="color: red;">Note 1: `developments.py` contains test environment keys which do not work to run PyNance on.</span><br/>
<span style="color: red;">Note 2: `production.py` contains `SQLALCHEMY_DATABASE_URI`, do not change this URL or you will break your docker environment.</span>

In order to switch the environment you need to open the file `/pynance-webinterface/backend/config/__init__.py`. This file contains a variable `DEBUG`. When **True** It makes use of the `development` environement. When **False** it will make use of the `production` environment.

<span style="color:red;">When building with docker you need to have the production environment enabled</span>

## <a name="pynance-installation"></a>PyNance Installation

scp -r PyNance-Webinterface server@192.168.178.213:/home/server/pynance-webinterface
