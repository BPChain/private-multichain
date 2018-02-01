#!/bin/sh +x

sleep 10
multichaind bpchain@masternode:7777 -printtoconsole &
python3 data_reader.py