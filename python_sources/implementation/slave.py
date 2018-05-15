"""I provide the Slave Proxy to communicate with the Blockchain slaves"""

from Savoir import Savoir
from bp_orchestrator import AbstractSlave

from python_sources.implementation.setup import Setup
from python_sources.project_logger import set_up_logging

LOG = set_up_logging(__name__)


class Slave(AbstractSlave):
    """I provide communication with a multichain slave"""

    def __init__(self, config, multichain_setup: Setup):
        super().__init__(config, multichain_setup)
        user = config['user']
        password = config['password']
        host = config['host']
        rpc_port = config['rpc_port']
        self.__rpc = Savoir(user, password, host, rpc_port, "bpchain")
        multichain_setup.prepare(self.__rpc)

    def is_alive(self):
        try:
            self.__rpc.getinfo()
            return True
            # pylint: disable=broad-except
        except Exception as error:
            LOG.warning('cannot reach %s. Error: %s Removing...', self.__rpc, error)
            return False

    def transact(self, name, hex_string):
        self.__rpc.publish('root', name, hex_string)
