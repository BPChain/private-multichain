"""I receive multichain username and password from slave nodes to control their local
multichain instance """

import rpyc
from Savoir import Savoir

from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)

chainnodes = []

class MasterService(rpyc.Service):
    # Do not use __init__ because of rpyc-library

    def on_connect(self):
        print("New Connection")

    def on_disconnect(self):
        print("Connection closed")

    def exposed_set_chainnodes(self, user, password, rpc_port):
        global chainnodes
        chain_node = Savoir(user, password, "privatemultichain_slavenode_" + str(len(chainnodes)+ 1), rpc_port, "bpchain")
        chainnodes.append(chain_node)
        LOG.info("Added connection to slave %d", len(chainnodes))
        return chain_node

    def exposed_close(self, chainnode):
        global chainnodes
        chainnodes.remove(chainnode)
