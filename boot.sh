#!/bin/sh
exec gunicorn --bind 0.0.0.0:$PORT mandel:app