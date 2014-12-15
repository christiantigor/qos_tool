#!/bin/sh
date >>/home/pi/dev/qos_tool_pi/crondate.txt
cd /
cd home/pi/dev/qos_tool_pi
python checkqos.py &
