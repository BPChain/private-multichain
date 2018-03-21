#!/bin/sh +x

sleep 20
multichaind bpchain@masternode:7777 -printtoconsole &
python3 -m python_sources.data_acquisition.data_acquisition.py &
python3 -m python_sources.slave_node.slave
