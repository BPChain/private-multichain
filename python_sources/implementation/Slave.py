from typing import Dict
from time import sleep
from Savoir import Savoir

from python_sources.implementation import Setup
from python_sources.project_logger import set_up_logging

LOG = set_up_logging(__name__)


class Slave:
    def __init__(self, config: Dict, setup: Setup):
        pass

    def is_alive(self):
        pass

    def transact(self, name, hex_string):
        pass

    @classmethod
    def get_new(cls, config, setup: Setup):
        return MultichainSlave(config, setup)


class MultichainSlave(Slave):

    def __init__(self, config, setup: Setup):
        super().__init__(config, setup)
        user = config['user']
        password = config['password']
        host = config['host']
        rpc_port = config['rpc_port']
        self.__rpc = Savoir(user, password, host, rpc_port, "bpchain")
        setup.prepare(self.__rpc)

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
