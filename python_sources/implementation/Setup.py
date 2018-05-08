from json import JSONDecodeError

from python_sources.data_acquisition.data_acquisition import connect_to_multichain
from time import sleep

from python_sources.project_logger import set_up_logging

LOG = set_up_logging(__name__)


class Setup:

    def __init__(self):
        self.chain_rpc = connect_to_multichain()
        self.height = 0
        LOG.info('::::::::::::Issued meta asset inital')

    def prepare(self, slave):
        self.grant_rights(slave, ['receive', 'send', 'mine'])
        LOG.info('prepared slaves %s', slave)

    def grant_rights(self, chain_node, rights):
        self.synchronize_heights(chain_node)
        for right in rights:
            self.chain_rpc.grant(chain_node.getaddresses()[0], right)


    def update_height(self, sender):
        is_updated = False
        while not is_updated:
            if sender.getmempoolinfo()['size'] == 0:
                self.height = self.local_height_from(sender)
                is_updated = True
            sleep(2)

    def synchronize_heights(self, sender):
        is_synced = False
        while not is_synced:
            if self.local_height_from(sender) >= self.height:
                is_synced = True
            sleep(2)

    def local_height_from(self, sender):
        successful = False
        while not successful:
            try:
                return sender.listblocks('-1')[0]['height']
            except (IndexError, KeyError, JSONDecodeError) as error:
                LOG.warning(error)
                sleep(5)
