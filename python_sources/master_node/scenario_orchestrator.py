"""I orchestrate a scenario on the multichain. To achieve that I use my local admin Multichain
instance as well as the remote multichain Instances of the slaves via json-rpc."""

from time import sleep

from ..data_acquisition.data_acquisition import connect_to_multichain
from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)


class ScenarioOrchestrator:
    """I hold all the Savoir instances for remote and my local admin nodes."""

    def __init__(self):
        self.chain_nodes = []
        self.chain_rpc = connect_to_multichain()
        self.groups = {}
        self.height = 0

    def grant_rights(self, chain_node, rights, label):
        self.synchronize_heights(chain_node)
        for right in rights:
            self.chain_rpc.grant(chain_node.getaddresses()[0], right)
        if label not in self.groups:
            self.groups[label] = []
        self.groups[label].append(chain_node)

    def issue_assets(self, asset_name, quantity, units, issue_more_allowed):
        self.chain_rpc.issue(self.chain_rpc.getaddresses()[0],
                             {'name': asset_name, 'open': issue_more_allowed}, quantity, units)
        self.update_height(self.chain_rpc)

    def issue_more(self, asset_name, quantity):
        self.synchronize_heights(self.chain_rpc)
        self.chain_rpc.issuemore(self.chain_rpc.getaddresses()[0], asset_name, quantity)
        self.update_height(self.chain_rpc)

    def send_assets(self, sender, recipient, asset_name, quantity):
        self.synchronize_heights(sender)
        LOG.info("Send assets from %s to %s", sender, recipient)
        sender.sendasset(recipient.getaddresses()[0], asset_name, quantity)
        self.update_height(sender)

    def send_assets_to_group(self, sender, recipient_group, asset_name, quantity):
        self.synchronize_heights(sender)
        if recipient_group in self.groups.keys():
            for member in self.groups[recipient_group]:
                self.send_assets(sender, member, asset_name, quantity)
            self.update_height(sender)

    def revoke_rights(self, chain_node, rights):
        self.synchronize_heights(self.chain_rpc)
        for right in rights:
            self.chain_rpc.revoke(chain_node.getaddresses()[0], right)

    def revoke_rights_from_group(self, group, rights):
        self.synchronize_heights(self.chain_rpc)
        for member in self.groups[group]:
            for right in rights:
                self.chain_rpc.revoke(member.getaddresses()[0], right)
        self.update_height(self.chain_rpc)

    def get_total_balance(self, sender):
        return sender.gettotalbalances()

    def get_quantity_of_asset(self, sender, asset_name):
        self.synchronize_heights(sender)
        total_balances = self.get_total_balance(sender)
        for balance in total_balances:
            if asset_name in balance.values():
                return float(balance['qty'])
        return 0

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
        return sender.listblocks('-1')[0]['height']


if __name__ == '__main__':
    ScenarioOrchestrator()
