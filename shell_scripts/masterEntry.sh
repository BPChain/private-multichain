#!/bin/sh +x
multichain-util create bpchain -anyone-can-connect=true
multichaind bpchain -printtoconsole &
python3 python_sources/data_acquisition/data_acquisition.py &
python3 -m python_sources.scenario_evap_coin 15
# Number passed to scenario must be >= number of slaves and number of members required in scenario
