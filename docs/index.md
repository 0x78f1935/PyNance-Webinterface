<span style="font-family:Papyrus; font-size:4em;"> PyNance </span>
<hr/>
<span style="font-family:Papyrus; font-size:2em;color:red;">Scammers are very active in the crypto market. PyNance will never ask  for your contact details. Avoid any other repository that claims to be PyNance which also is a Binance trading bot. Trade safe.</span>
<hr/>
<a name="Disclaimer"></a><span style="font-family:Papyrus; font-size:3em;color:red;">DISCLAIMER</span><br/>
<span style="font-family:Papyrus; font-size:2.5em;color:red;"> This tool is not a money printing tool and contains risks. </span><br/>
You are <strong> responsible</strong> for <strong>your own money and actions.</strong> <br/><br/><strong>By using this tool you agree to take FULL responsibility of your own money. </strong><br/> Even if this would mean missed opportunities caused by the algorithm of this bot or worse; <strong style="color:red;">losses</strong>. <br/><br/><strong style="color:green;">Be responsible</strong>, Only trade with money you can afford to lose.<br/>Take chances, Make mistakes, Get messy.... To the moon! <br/><br/><hr/>

<span style="font-family:Papyrus; font-size:3em;color:red;">IMPORTANT NOTICE</span><br/>

This tool makes use of docker. Once a running container has been established and the port of your machine is public. everyone in the same network will be able to connect to PyNance. <span style="color:red;">The current version of PyNance has no login screen.</span> You can secure yourself if you host PyNance on the machine you would like to check the interface on. Just make sure to block the port PyNance is running on.<br/><br/>Please do note; When creating your API key you should only allow it to work if the traffic send to Binance is comming from your IP address. This does <strong style="color:orange;">not</strong> fix the problem described above.<hr/>

# <a name="table-of-contents"></a>Table of Contents
1. [Table of Contents](#table-of-contents)
2. [Disclaimer](#Disclaimer)
3. [Quick Start](#quick-start)
4. [Why PyNance](#why)
5. [Requirements & Dependencies](#req)
    * [Production Req and Dep](#req-prod)
        - [Binance Account](#binance-account)
        - [Binance API Credentials](#binance-api)
        - [PyNance Configuration](#pynance-config)
        - [PyNance Installation](#pynance-installation)
    * [Development Req and Dep](#req-dev)
        - [(win10) NVM](#install-nvm)
        - [(win10) Node](#install-node)
        - [(win10) Python](#install-py)
        - [(win10) PyNance Core](#install-pynance-core)
        - [(win10) PyNance Web Interface](#install-pynance-web)
        - [(win10) PyNance Listener](#install-pynance-listener)
        - [(win10) MySQL](#install-mysql)
        - [PyNance Configuration](#install-configuration)
6. [Get Started](#get-started)
    - [Binance Account](#binance-account)
    - [Binance API Credentials](#binance-api)
    - [PyNance Configuration](#pynance-config)
    - [PyNance Installation](#pynance-installation)
7. [PyNance Configuration](#install-configuration)
    * [Localization](#localization)
    * [Database Password](#database-pass)
8. [PyNance Backups](#pynance-backups)
9. [Frequently Asked Questions](#faq)
10. [Community](#community)

# <a name="Community"></a>Quick start
- Make sure you have a [binance account](#binance-account) with [API credentials](#binance-api).
- Make sure you have [docker installed](#req)
- Copy and paste your [API credentials](#binance-api) into [/pynance-webinterface/backend/config/production.py](#pynance-config)
- Open a terminal in the root folder of the project and [deploy the containers](#pynance-installation)
- profit.

# <a name="why"></a>Why PyNance

Binance is a crypto exchange which allows you to trade crypto currency. I got tired of looking at graphs all day to manage my stop limits so naturally I tried to figure out ways to automate this process. I found a couple of Python libraries which talked to the Binance api. The required dependencies looked a little weird to me so I decided to make my own Binance library. This library only has one dependency: `requests`. After playing around with it I created the very first PyNance bot based on this library. Some friends got interested but didn't knew how to code. I took this as one of my weekend projects which I usually schedule to not get bored and created this complete webinterface around it. The goal of PyNance is to swingtrade crypto currency. Create buy orders when the price is low, and sells when the price is high. This bot is more patient than you do!

# <a name="req"></a>Requirements & Dependencies

## <a name="req"></a>Production requirements & dependencies

You basically can run PyNance anywhere where docker is installed. If you don't have docker installed yet make sure to install the [latest version](https://www.docker.com/get-started). Once docker is installed you are all set. The only thing left to do is to configure PyNance so it will accept your API credentials. You can read more on that topic in [Get Started](#get-started).


## <a name="req"></a>Development requirements & dependencies

### <a name="install-nvm"></a>nvm

In order to compile the frontend I personally use [NVM](https://github.com/nvm-sh/nvm). Its recommended to use version `12.20.1` of node.

    nvm install 12.20.1
    nvm use 12.20.1

### <a name="install-node"></a>node

When node is installed open a terminal and navigate toe `/pynance-webinterface/frontend`. From here you can compile the frontend.

    npm install
    npm run build

`npm run build` is used when building the docker environment. To enable hot reload for development purpose I recommend to use `npm run watch` instead.

### <a name="install-py"></a>python

Pynance exists out of three different parts; `PyNance-Core`, `PyNance-Webinterface` and `PyNance-Listener`. All three of those elements need to be created and / or configured in order to enable the development environment.

#### <a name="install-pynance-core"></a>PyNance-Core

Open a terminal and navigate to `/pynance-webinterface`. To keep things organized we start of with a virtualenvironment.

    python -m pip install virtualenv
    python -m virtualenv venv
    venv/Scripts/activate

Once the virtualenvironment is installed and activated navigate to `/pynance-webinterface/backend/plugins/PyNance`. Make sure you have the latest version! `git pull` can be used here.

Install the build requirements needed to build PyNance.

    pip install -r requirements.txt

Once the requirements for `PyNance-core` are installed you can execute the following command to compile the **.whl** package.

    python -m build

If `PyNance-core` has been successfully compiled navigate to `/pynance-webinterface/backend/plugins/PyNance/dist`. Here you should be able to see a file which is generated by the previous build step. The file has a name along the lines of: `PyNance-x.x.x-py3-none-any.whl`. Install it with pip! 

    pip install PyNance-x.x.x-py3-none-any.whl

#### <a name="install-pynance-web"></a>PyNance-Webinterface

Once the package is installed we can continue with `PyNance-Webinterface` requirements. Navigate back to the `/pynance-webinterface` root folder and open the `requirements.txt` with a text editor. Comment out the line that points to the **.whl** package. Don't remove it. You need to uncomment it when building a docker environment. Check if the version is the same as the version you just had build. Here I show how it should look like.

    ...
    # PyNance @ file:///workspaceFolder/backend/plugins/PyNance/dist/PyNance-0.0.1-py3-none-any.whl
    ...

Save the file and go back to you terminal. Install the requirements.

    pip install -r requirements.txt

Open the `requirements.txt` file again with your texteditor to make sure you uncomment that line again.

    ...
    PyNance @ file:///workspaceFolder/backend/plugins/PyNance/dist/PyNance-0.0.1-py3-none-any.whl
    ...

#### <a name="install-pynance-listener"></a>PyNance-Listener

If this is all done we can move on to the `PyNance-Listener`. This one is easy and we will discuss the `PyNance-Listener` in the configuration section since there is not much to tell about.

### <a name="install-mysql"></a>MySql

[MySQL](https://www.mysql.com/) is used to keep track of the orders the bot placed in the past. We also use the database as a way to prevent beind [rate-limited by the binance api](https://www.binance.com/en/support/faq/360004492232). The production build comes with a MySQL environment build in. But to develop you might want to setup a local database real quick. This can be done with docker and since docker gives that much advantage I expect you have it installed at this point. Execute the following code to quickly setup a mysql database.

    docker pull mysql/mysql-server:latest
    docker run --name=mysql --restart on-failure -p 3306:3306 -d mysql/mysql-server:latest
    docker logs --follow mysql

    Note: Look for the root password
    (
        if docker logs if to much for you:
        `docker logs mysql 2>&1 | grep GENERATED`
    )

    docker exec -it mysql mysql -u root -p

    >>> Provide password

    mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';
    mysql> CREATE USER 'user'@'%' IDENTIFIED BY 'admin';
    mysql> GRANT ALL PRIVILEGES ON *.* TO 'user'@'%';
    mysql> FLUSH PRIVILEGES;

    Connection string: 
    `mysql+pymysql://user:admin@127.0.0.1:3306/webserver`

The connection string can be placed in `/pynance-webinterface/backend/config/developments.py` under the `SQLALCHEMY_DATABASE_URI` variable. The production database will run on port `3307`.

`PyNance-Webinterface` makes use of migrations to setup the tables in the database. You can achieve the same in a terminal where the virtualenvironment is activated.

    set FLASK_APP=webserver.py
    flask db init
    flassk db migrate
    flask db upgrade

## <a name="install-configuration"></a>Configuration

Outside the normal configuration described [here](#pynance-config) there are still a couple of variables to play with. <span style="color:orange">The following files contain a variable called `DEBUG` which are required to be `False` when building the production environment.</span> This is imporant. Otherwise your docker build will fail.

 - /pynance-webinterface/listener.py
 - /pynance-webinterface/backend/config/\_\_init\_\_.py

# <a name="localization"></a>Localization

Thanks to a small but amazing community PyNance is currently translated into 3 different languages other then English.

1. Dutch (nl)
2. Filipino (fil)
3. French (fr)

Default: English (en)

If you would like to be part of the community, you can! [You can join here](https://discord.gg/qmb7PG9r2c). You can change the default localization in `/pynance-webinterface/.env.development` or in `/pynance-webinterface/.env.production`.

# <a name="database-pass"></a>Database Password

The default password for the database is available to anyone that has access to this repo. <span style="color:red">Make sure to change the database password to stay secure.</span> You can find the password in the `/pynance-webinterface/docker-compose.yaml`. If you change the password you should also update it in the file `/pynance-webinterface/backend/config/production.py`


# <a name="get-started"></a>Get Started

Before we get started with PyNance I think its a good idea to explain the fundamentals of this bot. Once PyNance is installed you will be able to sellect two different kinds of currencies. **currency_1** and **currency_2**. PyNance will glue those two currencies together to form a `symbol`.
A symbol can look like `ADABUSD` or like `BTCUSDT`. Lets say we pick `BTCUSDT` that would mean, in order to start PyNance <span style="color:red">we need an available BTC balance in your spot wallet to be able to trade.</span> Once PyNance is online, it will look if the current value of ***in our case BTCUSDT*** is lower then the average price. If this is the case PyNance will buy (100% - minimal profit %) calculated over <span style="colr:red">the current amount available in your spot wallet</span>. This is the amount PyNance places a buy entry for. If PyNance was able to successfully bought some crypto it will switch its state to sale and starts selling the crypto. PyNance is patient and will hold the amount bought until the price is met, which is calculated based on the minimal profit percentage. <span style="color:green;">Profit is calculated excluding fees.</span> Fees are calculated in the buy-in price. If you like to FOMO for some weird reason but your funds are locked away because PyNance is running,.. No worry. PyNance got you covered. There is a "Panik" button, Once active PyNance will try to sell its crypto off without looking at profit. However It only sells when the current price is higher then the (bought-in price + costs of the fee). This way you can FOMO a little bit more secure without to much loss. Once Panik is active PyNance halts the procedure to buy new coins. When PyNance is selling it will sell all the balance which is available. In this example that would be all the `USDT` available. Then the cycle continues!

<span style="color:red">When you start the bot for the first time Check yourself for a good entry in the binance app. This is important since each configuration can have different results</span>

## <a name="binance-account"></a>Binance Account

In order to fetch the latest market information and to be able to place orders you will need a Binance account. [You can create an account here](https://www.binance.com/en/register?ref=73051759). This account also contains your wallets and API credentials. Make sure to enable 2factor authentication.

## <a name="binance-api"></a>Binance API Credentials

After you have created your [binance account](#binance-account) you need to create your API credentials. Once created make sure to save them. The secret is hidden after creation and you need the secret in order to proceed. [You can follow the steps on how to create API credentials here](https://www.binance.com/en/support/faq/360002502072-How-to-create-API).

## <a name="pynance-config"></a>PyNance Configuration

There are two environments available to you. `production` and `development`. Both environments work the exact same way. The main difference is that `production` should be used in the `docker environment`.. You can ignore changes for git using the following command: `git update-index --assume-unchanged backend/config/production.py`

Navigate to the following path `/pynance-webinterface/backend/config`. \
In this location you should have atleast two files. `development.py` and `production.py` which represents those environments. `BINANCE_API_KEY` and `BINANCE_API_SECRET` are the two values which should contain your API credentials obtained from [Binance](#binance-api).

<span style="color: red;">Note 1: `developments.py` contains test environment keys which do not work to run PyNance on.</span><br/>
<span style="color: red;">Note 2: `production.py` contains `SQLALCHEMY_DATABASE_URI`, do not change this URL or you will break your docker environment.</span>

In order to switch the environment you need to open the file `/pynance-webinterface/backend/config/__init__.py`. This file contains a variable `DEBUG`. When **True** It makes use of the `development` environement. When **False** it will make use of the `production` environment.

<span style="color:red;">When building with docker you need to have the production environment enabled</span>

## <a name="pynance-installation"></a>PyNance Installation

In this case we ignore the development environment for now and we make this a point of attention in the advanced section of this documentation. Once the [dependencies](#req) are installed and the [configuration](#pynance-config) is configured for `production` we can finally start the installation. Open a terminal and navigate to `/pynance-webinterface` root folder. Execute the following command:

    docker-compose up --build -d

This will take a moment depending on your hardware. Once finished you should be able to type normally in the terminal again. Check if everything is `up` (4 containers) with the following command.

    docker ps -a

And your done! It's that simple. Open up your favorite browser (recommended: google chrome) and navigate to: [http://127.0.0.1:1337/](http://127.0.0.1:1337/).

# <a name="pynance-backups"></a>Backups

The docker environment is configured so the data in the `MySQL` database is stored on disk and not locked away in docker itself. This should mean that whenever you `git pull` the latest version you should keep your data in the database. The data can be found in `/pynance-webinterface/backend/config/docker/database/backup`.

# <a name="faq"></a>Frequently Asked Questions

- I recieve the error: `standard_init_linux.go:190: exec user process caused "no such file or directory"`. What should I do?
    *   You can read more on how to solve this issue [here](https://stackoverflow.com/questions/51508150/standard-init-linux-go190-exec-user-process-caused-no-such-file-or-directory)

- If there is a trade ongoing and the bot senses that there is a good entry will it buy again?
    * No

- I see an error message about the database not able to reach, what can i do to fix this?
    *   Patience, wait until your environment is ready to go.

- The bot keeps losing connection. What can I do?
    * Make sure you are on a stable internet line. Wifi is not recommended.

- Can I trade multiple currencies at the same time?
    * No, The bot only trades what is selected in the configuration panel.

- Can I switch symbols while the bot is trading?
    * Yes, the bot keeps track of what it traded. Just make sure you have the funds available in your wallet.

- Can I run multiple instances of PyNance?
    * No, In theory you could... But Binance will ban your API credentials based on their ratelimit. MAX 1 instance.

- How do i QUIT a trade!?
    * Binance is LAW. You can at anytime access your portfolio within Binance. Make sure the bot is offline or it will keep trading your funds. Keep in mind if you trade manually within Binance your Database might get out of sync with Binance.

- I am unable to choose between currencies, what now?
    * Make sure your API credentials are correct.

- I still seem to have issues with my API key. What can i check to hopefully fix this issue?
    * Check if your API key has the following API restrictions enabled: `Enable Reading` and `Enable Spot & Margin Trading`

# <a name="Community"></a>Community

If you still manage to get stuck, want to keep updated with the latests updates or flex your profit with other botters you can!. [Join our discord!](https://discord.gg/qmb7PG9r2c)
