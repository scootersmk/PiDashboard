#!/bin/bash

cd /home/pi/PiDashboard
source venv/bin/activate
#Sets API_KEY env variable
source secret.sh
./run.py --mode forever
