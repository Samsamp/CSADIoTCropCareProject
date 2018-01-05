#!/bin/bash

sudo hologram network connect

tmux new-session -d -s IoT 'sudo python /home/pi/Documents/CSADIoTCropCareProject/Project/main.py'
