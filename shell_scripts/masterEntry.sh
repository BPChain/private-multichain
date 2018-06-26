#!/bin/bash +x
multichain-util create bpchain -anyone-can-connect=true
sed -i 's/target-block-time = 15/target-block-time = 10/g' /root/.multichain/bpchain/params.dat
sed -i 's/maximum-block-size = 8388608/maximum-block-size = 1000000000/g' /root/.multichain/bpchain/params.dat
multichaind bpchain -printtoconsole &
python3 -m python_sources.data_acquisition.data_collection 0 &
python3 -m python_sources.master.run_scenario_service
