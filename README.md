# private-multichain
Dev-Branch: [![Maintainability](https://api.codeclimate.com/v1/badges/0f8141a9f162b0f52679/maintainability)](https://codeclimate.com/github/BPChain/private-multichain/maintainability)
[![Build Status](https://travis-ci.org/BPChain/private-multichain.svg?branch=dev)](https://travis-ci.org/BPChain/private-multichain)
<br>
Master-Branch: [![Build Status](https://travis-ci.org/BPChain/private-multichain.svg?branch=master)](https://travis-ci.org/BPChain/private-multichain)
### Structure
Run Multichain in Docker. The module comprised of four packages. <br>
The general idea is that one node is a master node controlling and deploying the scenario and all 
other nodes are slavenodes executing the transactions required by that scenario. 

### Python files
1. [`data_acquisition`](./python_sources/data_acquisition) which sends the runtime data of the chain
to a server. 
2. [`implementation`](./python_sources/implementation) which offers proxy implementations for the slave nodes 
which allows the 
master-node to communicate with the slaves. It also offers a `setup` class to perform actions such
 as rights management on the blockchain.
3. [`master`](./python_sources/master) contains the main entry point to start the 
[`scenario-orchestration-service`](https://github.com/BPChain/scenario-orchestration-service) which 
listens for input from the [`private-chain-controller` ](https://github.com/BPChain/private-chain-controller)
at port 21000. 
4. [`slave_node`](./python_sources/slave_node) which contains a python program running on the 
each slave. It connects to the `scenario-orchestration-service` running on the [`master`](
./python_sources/master) to send its credentials for multichain rpc login. 

### Docker Setup
Both slave and master share one dockerfile but are defined as different services with different 
entry points in the docker-compose file. You can simply scale slaves at any time. Masternodes 
should not be scaled. 
Run e.g. docker-compose up --build scale slavenode=15



##### Miscellaneous
This Multichain setup is not recommended for production. Anyone can control the nodes.
