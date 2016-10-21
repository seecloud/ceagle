#!/bin/sh

if test "${CEAGLE_WITH_GUNICORN}" = 1
then
   gunicorn -w 4 -b 127.0.0.1:5000 ceagle.wsgi:app
else
   export FLASK_APP=ceagle.wsgi
   export FLASK_DEBUG=1
   flask run
fi
