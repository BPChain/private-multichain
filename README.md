# private-multichain
Dev-Branch: [![Maintainability](https://api.codeclimate.com/v1/badges/0f8141a9f162b0f52679/maintainability)](https://codeclimate.com/github/BPChain/private-multichain/maintainability)
Master-Branch: [![Build Status](https://travis-ci.org/BPChain/private-multichain.svg?branch=master)](https://travis-ci.org/BPChain/private-multichain)

Run Multichain in Docker. The setup is comprised of three parts.
1. `data_acquisition` which sends the runtime data of the chain
to a server 
2. `slavenode` which allows the master node to connect
to query their username and password of their multichain instance.
3. `master_node` can control the admin node in the blockchain and functions as a central 
controller for a scenario which can be run on the blockchain. Such a scenario can
be defined in a file in `master-node`


##### Docker Setup
In the docker compose setup we usually have multiple slave nodes running
`slave_node` and one node running `master_node`.

There exists only one docker file however the entrypoints for the master and slave nodes are 
different.

You have to specify the number of slave nodes a priori in ``masterEntry.sh`` and then
scale to that number in docker compose.

##### How to run
docker-compose up --build scale slavenode=15

### Miscellaneous
This Multichain setup is not recommended for production. Anyone can control the nodes.

Do not forget to pip freeze > requirements.txt if you add new dependencies.
