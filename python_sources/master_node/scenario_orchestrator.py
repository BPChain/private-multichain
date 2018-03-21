"""I orchestrate a scenario on the multichain. To achieve that I use my local admin Multichain
instance as well as the remote multichain Instances of the slaves via json-rpc."""

from socket import gaierror
from time import sleep
import logging
import sys

import rpyc
from Savoir import Savoir
from ..data_acquisition.data_acquisition import connect_to_multichain


def set_up_logging():
    new_logger = logging.getLogger(__name__)
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s | In: %(module)s at: %(lineno)d')
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    new_logger.setLevel(logging.INFO)
    new_logger.addHandler(console)
    return new_logger


LOG = set_up_logging()


class ScenarioOrchestrator:
    """I hold all the Savoir instances for remote and my local admin nodes."""

    def __init__(self):
        self.chain_nodes = []
        self.chain_rpc = connect_to_multichain()
        self.groups = {}
        self.height = 0
        LOG.info("Orchestrator is ready for connections")

    def connect_to_slaves(self, number_of_slaves):
        sleep(40)
        unconnected_ids = list(range(1, number_of_slaves + 1))
        while unconnected_ids:
            slave_id = unconnected_ids.pop(0)
            try:
                connection = rpyc.connect("privatemultichain_slavenode_" + str(slave_id), 60000)
                user, password, rpc_port = connection.root.get_credentials()
                chain_node = Savoir(user, password, "privatemultichain_slavenode_" + str(slave_id),
                                    rpc_port, "bpchain")
                self.chain_nodes.append(chain_node)
                LOG.info("Added connection to %d", slave_id)
            except ConnectionRefusedError:
                unconnected_ids.append(slave_id)
                LOG.warning("Could not connect to %d. retry later", slave_id)
            except gaierror:
                LOG.warning("Could not resolve node %d. removing id", slave_id)
            except Exception as unknown_exception:
                LOG.error("Something went very wrong: %s", unknown_exception)
                sleep(10)

    def grant_rights(self, number, rights, label):
        if number > len(self.chain_nodes):
            LOG.error("Not enough Nodes. Requested %d had %d", number, len(self.chain_nodes))
            sys.exit(1)
        else:
            self.groups[label] = []
            for _ in range(number):
                chain_node = self.chain_nodes.pop(0)
                for right in rights:
                    self.chain_rpc.grant(chain_node.getaddresses()[0], right)
                self.groups[label].append(chain_node)

    def issue_assets(self, asset_name, quantity, units, issue_more_allowed):
        self.chain_rpc.issue(self.chain_rpc.getaddresses()[0],
                             {'name': asset_name, 'open': issue_more_allowed}, quantity, units)
        self.get_height_after(self.chain_rpc)

    def issue_more(self, asset_name, quantity):
        if not self.is_blocked(self.chain_rpc):
            self.chain_rpc.issuemore(self.chain_rpc.getaddresses()[0], asset_name, quantity)
            self.get_height_after(self.chain_rpc)

    def send_assets(self, sender, recipient, asset_name, quantity):
        if not self.is_blocked(sender):
            LOG.info("Send assets from %s to %s", sender, recipient)
            sender.sendasset(recipient.getaddresses()[0], asset_name, quantity)
            self.get_height_after(sender)

    def send_assets_to_group(self, sender, recipient_group, asset_name, quantity):
        if not self.is_blocked(sender):
            for member in self.groups[recipient_group]:
                self.send_assets(sender, member, asset_name, quantity)
            self.get_height_after(sender)

    def revoke_rights(self, group, rights):
        if not self.is_blocked(self.chain_rpc):
            for member in self.groups[group]:
                for right in rights:
                    self.chain_rpc.revoke(member.getaddresses()[0], right)
            self.get_height_after(self.chain_rpc)

    def get_total_balance(self, sender):
        return sender.gettotalbalances()

    def get_quantity_of_asset(self, sender, asset_name):
        if not self.is_blocked(sender):
            total_balances = self.get_total_balance(sender)
            for balance in total_balances:
                if asset_name in balance.values():
                    return float(balance['qty'])
            return 0

    def get_height_after(self, sender):
        while True:
            if sender.getmempoolinfo()['size'] == 0:
                self.height = self.get_height(sender)
                return

    def is_blocked(self, sender):
        while True:
            if self.get_height(sender) >= self.height:
                return False

    def get_height(self, sender):
        return sender.listblocks('-1')[0]['height']

if __name__ == '__main__':
    ScenarioOrchestrator()
