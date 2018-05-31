"""I offer a Setup Class that provides basic setup for slaves and the scenario"""

from json import JSONDecodeError
from time import sleep

from bp_orchestrator import AbstractSetup

from python_sources.data_acquisition.multichain_connector import connect_to_multichain
from python_sources.project_logger import set_up_logging

LOG = set_up_logging(__name__)


class Setup(AbstractSetup):
    """I provide basic setup such as rights management and stream creation for the scenario and the
    slaves"""

    def __init__(self):
        super().__init__()
        self.chain_rpc = connect_to_multichain()
        self.height = 0
        LOG.info('::::::::::::Issued meta asset inital')

    def prepare(self, slave):
        self.__grant_rights(slave, ['receive', 'send', 'mine'])
        LOG.info('prepared slaves %s', slave)

    def __grant_rights(self, chain_node, rights):
        self.__synchronize_heights(chain_node)
        for right in rights:
            self.chain_rpc.grant(chain_node.getaddresses()[0], right)

    def __update_height(self, sender):
        is_updated = False
        while not is_updated:
            if sender.getmempoolinfo()['size'] == 0:
                self.height = self.__local_height_from(sender)
                is_updated = True
            sleep(2)

    def __synchronize_heights(self, sender):
        is_synced = False
        while not is_synced:
            if self.__local_height_from(sender) >= self.height:
                is_synced = True
            sleep(2)

    def __local_height_from(self, sender):
        successful = False
        while not successful:
            try:
                return sender.listblocks('-1')[0]['height']
            except (IndexError, KeyError, JSONDecodeError) as error:
                LOG.warning(error)
                sleep(5)
