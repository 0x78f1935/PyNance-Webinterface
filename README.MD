## PyNance

<div class="text-white bg-blue mb-2">
  CAUTION

  Scammers are very active in the crypto space. PyNance will never ask for your contact details nor account information. 
  PyNance relies on your **API credentials** which should be located in `.env.production`. Avoid any other repository that claims to be PyNance which tries to mimic the original. The original repo is `github.com/0x78f1935/PyNance-Webinterface`. Trade with caution,... Trade safe.
</div>

# <a name="disclaimer"></a> Disclaimer

PyNance is not a money printing tool. You are responsible for your own trades. When using this tool you agree that you take full responsibility of your whole portfolio, money and trades. You also declare that you have read the `LICENSE` included with **PyNance**. **PyNance** comes without any warrenty. A **loss** is still a **loss**.

<div class="text-white bg-blue mb-2">
  Only trade with money you can afford to loss. Take chances, Make mistakes, Get messy.... To the moon! 🚀
</div><br/>

# <a name="pre-read"></a>PRE-READ
Before we get started, this README file includes "two" editions. The First part will explain how PyNance works and how to get it running in a production build. This part of the readme file is ment for people who have no experience with code. The second part of this README file is ment for people that would like to modify PyNance to there likings. This wil part will show you how to setup a development environment.


(You can skip this) -> People who actually might have seen the previous documentation probably noticed the warning notice about the security risks involved with people on the same network. Version 2.0.0 introduces a new feature to solve this problem!. You can configure a `master key` within your **PyNance** dashboard to prevent people from accessing your **PyNance** dashboard and internal endpoints! More on that later. All you need to know for now is that it has been fixed!

# Table of Contents

1. [Disclaimer](#disclaimer)
2. [Pre read](#pre-read)
3. [Configure](#configure)
4. [Run PyNance](#run-pynance)
5. [Shutdown PyNance](#stop-pynance)
6. [Features](#features)
    - [Backups](#backups)
    - [Master Password](#masterpwd)
7. [Development Environment](#dev-build)
    1. [Requirements](#req)
        1. [NVM](#install-nvm)
        2. [Node](#install-node)
        3. [Python](#install-py)
            1. [Virtualenv](#virtualenv)
            2. [pip](#pip)
    2. [Listener](#listener)
    3. [Dashboard](#dashboard)
        1. [Backend](#backend)
        2. [Frontend](#frontend)
    4. [Database](#db)

# <a name="configure"></a>Configure PyNance
Open the `.env.production` file and read through it. You can look into `.env.development` for a working example. The following environment variables are important

| Variables                      	| Description                                                                                              	|
|--------------------------------	|----------------------------------------------------------------------------------------------------------	|
| ENVIRONMENT                    	| This environment variable can be ignored                                                                 	|
| BINANCE_API_KEY                	| Your Binance API Key, You can make an account [here](https://www.binance.com/en/register?ref=73051759)   	|
| BINANCE_API_SECRET             	| Your Binance API secret which matches your API Key                                                       	|
| LOCALE                         	| The default language of the application. You options are [en, nl, fr, fil]                               	|
| SQLALCHEMY_DATABASE_URI        	| This is the connection string to the internal database. You should change its password to be extra safe. 	|
| SQLALCHEMY_TRACK_MODIFICATIONS 	| Turn on or off database logging                                                                          	|

<br/>

# <a name="run-pynance"></a>Run PyNance

Its recommended to run **PyNance** in `production` mode with docker which you can [install here](https://docs.docker.com/get-docker/).
Once docker is configured correctly there is only one step between you and **PyNance**.
Open a terminal and navigate to the root directory of this project. Double check your `.env.production` file before executing the next step. The next step takes a while. Type in your terminal the following command to run **PyNance**

    docker-compose up --build -d

Give it a small moment, Once its all done you can check if everything is running with the following command

    docker ps -a

The output of `docker ps -a` should look something like this

    CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS                PORTS                                     NAMES
    fa31e026e461   pynance2_listener           "./entrypoint_listen…"   40 minutes ago   Up 40 minutes                                                   listener
    131dd63ead97   nginx:stable                "/docker-entrypoint.…"   40 minutes ago   Up 40 minutes         80/tcp, 0.0.0.0:1337->5000/tcp            nginx
    6ae3900af49f   pynance2_dashboard          "./backend/config/do…"   40 minutes ago   Up 40 minutes         5000/tcp                                  dashboard
    71e5c67d6108   pynance2_database           "docker-entrypoint.s…"   40 minutes ago   Up 40 minutes         3306/tcp, 33060/tcp                       database


To open the application navigate to https://127.0.0.1:1337.

If the containers have the status `Exited` for some reason you can just use `docker-compose up` without the `--build` option. This way you don't lose any data.

# <a name="stop-pynance"></a>Closing PyNance

In order to close PyNance on your computer use the following two commands in a terminal which has been set to the root directory of **PyNance**

    docker-compose down -v
    docker system prune

When you get asked to enter `(y/N)` type in `Y` and hit enter.
Everything should be clean right now.

If you have some issues with closing PyNance or building PyNance you might want to reset docker.
Be warned the `reset_docker.bat` cleans almost everything within docker. Images and containers.

<div class="text-white bg-blue mb-2">
  The following section will explain a bit more about the functionality within <strong>PyNance</strong>. For the development version <a href='#dev-build'>click here</a>
</div><br/>

# <a name="features"></a>Features

## <a name="backups"></a>Backups

Make regular backups. When you remove the containers you also will remove your data. By making a backup you only make a backup of the orders placed by **PyNance**. You can import the backup in any running instance to recover your orders which allows the bot to continue where it left off.

## <a name="masterpwd"></a>Master password

A master password can be set to prevent other users on the network from using your **PyNance** instance. There is no option in the UI to recover your lost password. Matter in fact, there is no option at all to recover a lost password since this is considered a security breach. When a master password is set, endpoints used internally will require a token in order to function. **PyNance** handles this all for you.

- But I still need to recover my password, what do I do?

There is only one method which allows you to reset the Master Password. This method works only locally on the computer where **PyNance** is running. Open a terminal and use `docker ps -a` in order to see all the container id's. copy the container id of the container `pynance2_dashboard` and enter the following command.

    docker exec -it 6ae3900af49f bash

Once inside the container, execute the following command to remove the master password

    flask password reset

## Other settings

**PyNance** will come with various settings so you can configure when the bot needs to place a buy or sell order. Make sure to read the tooltips.


<div class="text-white bg-blue mb-2">
  The following section will include information about the development environment. If you have a production setup up and running you can close the documenation here. The next part is for the nerds.
</div><br/>


# <a name="dev-build"></a>Development Build (localhost)

You can [configure](#configure) the development build just like the production build. Use the `.env.development` file instead.

## <a name="req"></a>Requirements & dependencies

### <a name="install-nvm"></a>nvm

In order to compile the frontend I personally use [NVM](https://github.com/nvm-sh/nvm). Its recommended to use version `12.20.1` of node.

    nvm install 12.20.1
    nvm use 12.20.1

### <a name="install-node"></a>node

When node is installed open a terminal and navigate to the `/frontend` folder. From here you can compile the frontend.

    npm install
    npm run build

`npm run build` is used when building the docker environment. To enable hot reload for development purpose I recommend to use `npm run watch` instead.

### <a name="install-py"></a>python

Pynance exists out of three different parts; `PyNance-Core`, `PyNance-Webinterface` and `PyNance-Listener`. All three of those elements need to be created and / or configured in order to enable the development environment. Since version `2.0.0` the `PyNance-Core` is included in the requirements.txt as a git repo.

#### <a name="virtualenv"></a>Virtualenv

Open a terminal and navigate to the root folder of this project. To keep things organized we start of with a virtualenvironment.

    python -m pip install virtualenv
    python -m virtualenv venv
    venv/Scripts/activate

#### <a name="pip"></a>install requirements

Open a terminal and navigate to the root folder of this project and install the requirements. Make sure your virtualenv is active.

    pip install -r requirements.txt

## <a name="listener"></a>Listener

The `PyNance-Listener` triggers an endpoint which do the work within docker. Once building a production environment you want the `debug` value in the `listener.py` to be **False**. If you are testing things locally you need to put this value on **True**. Just so you are calling the right endpoint.

## <a name="dashboard"></a>Dashboard

### <a name="backend"></a>Backend

The dasboard is quite simple to start but you need a working database in order to actually use it. To start the dashboard you can use flask. Flask is also used to initiate the database explained in the [database](#db) section. Open a terminal in the root directory of this project and use the following command to start the backend

    set FLASK_APP=webserver.py
    flask run

Make sure that the `debug` variable is set to **True** in the `backend/config/__init__.py` file when running the development environment

In visual studio code you could use the following debug config

    {
        // Use IntelliSense to learn about possible attributes.
        // Hover to view descriptions of existing attributes.
        // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Flask",
                "type": "python",
                "request": "launch",
                "module": "flask",
                "env": {
                    "FLASK_APP": "${workspaceFolder}/webserver.py",
                    "FLASK_ENV": "development",
                    "FLASK_DEBUG": "1"
                },
                "args": [
                    "run",
                    // "--no-debugger"
                ],
                "jinja": true
            }
        ]
    }

### <a name="frontend"></a>Frontend

Open a terminal in the `/frontend` folder of the root directory on this project. Make sure to install all the requirements for node.

    npm install

Once that is done you have a couple of options to play with

    # Hot reload
    npm run watch

    # Without hot reload or backend
    npm run serve

    # Production build
    npm run build

    # Check linting
    npm run lint

    # Fix linting
    npm run lint:fix

    # Check translation keys
    npm run i18n:report

The fronend needs to be compiled before using the backend.

## <a name="db"></a>Database

**PyNance** needs a database and a quick solution to run a local database would be docker.
You can follow the next steps to quickly throw up a database.


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
    `mysql+pymysql://user:admin@127.0.0.1:3306/scheme`

Once the database is set you can use **FLASK** to setup all the tables and such

    venv\Scripts\activate
    set FLASK_APP=webserver.py
    flask db init
    flask db migrate
    flask db upgrade