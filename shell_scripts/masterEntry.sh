#!/bin/sh +x
multichain-util create bpchain -anyone-can-connect=true
multichaind bpchain -printtoconsole &
python3 python_scripts/master.py
