#!/bin/bash +x
sleep 10
multichain-util create bpchain -anyone-can-connect=true
multichaind bpchain -printtoconsole&
python3 -m python_sources.data_acquisition.data_acquisition &
python3 -m python_sources.master.run_scenario_service
