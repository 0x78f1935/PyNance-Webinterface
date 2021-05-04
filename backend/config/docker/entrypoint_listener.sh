#!/bin/sh


while ! curl -o - pn_database:3306; do sleep 1; done

{
    python listener.py
}