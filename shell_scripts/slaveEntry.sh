#!/bin/sh +x

sleep 10
multichaind bpchain@masternode:7777 -printtoconsole &
python3 -m python_sources.slave_node.slave