#!/bin/sh +x

sleep 10
multichaind bpchain@masternode:7777 -printtoconsole &
python3 setup.py