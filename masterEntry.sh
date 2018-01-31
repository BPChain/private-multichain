#!/bin/sh +x
multichain-util create bpchain -anyone-can-connect=true
multichaind bpchain -printtoconsole
