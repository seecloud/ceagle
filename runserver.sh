#!/bin/bash

if test "${CEAGLE_WITH_GUNICORN}" = 1
then
    gunicorn -w 4 -b 127.0.0.1:5000 ceagle.main:app
else
    export FLASK_APP=ceagle.main
    export FLASK_DEBUG=1
    flask run
fi
