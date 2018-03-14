#!/bin/sh +x
multichain-util create bpchain -anyone-can-connect=true
multichaind bpchain -printtoconsole &
python3 -m python_sources.master_node.scenario_orchestrator
