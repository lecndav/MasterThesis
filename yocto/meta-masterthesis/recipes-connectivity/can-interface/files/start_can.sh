#!/bin/sh

echo "setting up can interfaces"

ip link set can0 up type can bitrate 500000 restart-ms 50 listen-only on
ip link set can0 qlen 50

exit 0
