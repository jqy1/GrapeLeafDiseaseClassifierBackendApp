#!/bin/sh
export FLASK_APP=run.py
export FLASK_DEBUG=1
#pipenv run flask -h 0.0.0.0 --port=8080
python run.py test