# binance
Binance bot trader

Inspired by https://www.youtube.com/watch?v=qk4gZrBR9CU

# UNITTESTS

You can run unittests by running

    python -m unittest

# BUILDING

You need to build a whl package.

    python -m build

# COPY TO SERVER

    scp -r D:\Private\PyNance server@192.168.178.213:/home/server/PyNance

## Debian10

    sudo apt-get install python3-dev
    sudo apt-get install python3-pip
    python3 -m pip install virtualenv
    python3 -m virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
