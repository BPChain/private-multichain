#!/bin/sh +x

sleep 10
multichaind bpchain@masternode:7777 -printtoconsole &
python3 python_sources/data_acquisition/data_acquisition.py &
python3 -m python_sources.slave_node.slave