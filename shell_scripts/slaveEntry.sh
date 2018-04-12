#!/bin/bash +x

sleep 20
multichaind bpchain@masternode:7777 &
python3 -m python_sources.slave_node.slave &
python3 -m python_sources.data_acquisition.data_acquisition
