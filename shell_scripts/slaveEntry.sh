#!/bin/sh +x

sleep 10
multichaind bpchain@masternode:7777 -printtoconsole &
python3 python_scripts/slave.py