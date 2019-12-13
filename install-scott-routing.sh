#!/bin/bash

venv=$VIRTUAL_ENV
if [ -z "$venv" ]; then
    echo "Seems to be no virtual env; please activate it first"
    exit
fi

scott=routing.py.scott
if [ ! -e $scott ]; then
    echo "I can't find $scott"
    exit
fi

sp="$venv/lib/python3.6/site-packages"
if [ ! -d $sp ]; then
    echo "I can't find $sp"
    exit
fi

cas="$sp/flask_cas"
if [ ! -d $cas ]; then
    echo "I can't find $cas"
    echo "Did you pip install flask_cas?"
    exit
fi

cp $scott $cas
cd $cas
mv routing.py routing.py.orig
ln -s routing.py.scott routing.py

