#!/bin/bash
cd /home/he/pzdiscord
nohup python3.8 main.py --config config.cfg >log.txt 2>&1 &
