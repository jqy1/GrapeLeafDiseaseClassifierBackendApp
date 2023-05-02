#!/bin/sh
ps -ef | grep 'python run.py run' | awk '{print $2}' | xargs kill -2