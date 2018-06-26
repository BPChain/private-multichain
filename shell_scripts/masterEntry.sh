#!/bin/bash +x
multichain-util create bpchain -anyone-can-connect=true
echo "target-block-time = 10\nmaximum-block-size = 1000000000 " >> /root/.multichain/bpchain/params.dat
multichaind bpchain -printtoconsole &
python3 -m python_sources.data_acquisition.data_collection 0 &
python3 -m python_sources.master.run_scenario_service
