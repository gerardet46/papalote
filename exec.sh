#!/usr/bin/bash

#p=$(ps aux | grep grep | awk '{print $2}')
pkill -f bot.py

./bot.py > debug.log 2>&1 &
