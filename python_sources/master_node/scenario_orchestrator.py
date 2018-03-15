import socket

import rpyc
from time import sleep
from Savoir import Savoir
from ..data_acquisition.data_acquisition import connect_to_multichain
import logging
import sys


def set_up_logging():
    logger = logging.getLogger(__name__)
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s | In: %(module)s at: %(lineno)d')
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(console)
    return logger


logger = set_up_logging()


class ScenarioOrchestrator:

    def __init__(self):
        self.chain_nodes = []
        self.chain_rpc = connect_to_multichain()
        self.groups = {}
        logger.info("Orchestrator is ready for connections")

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
                logger.info("Added connection to %d", slave_id)
            except ConnectionRefusedError:
                unconnected_ids.append(slave_id)
                logger.warning("Could not connect to %d. retry later", slave_id)
            except socket.gaierror:
                logger.warning("Could not resolve node %d. removing id", slave_id)
            except Exception as e:
                logger.error("Something went very wrong: %s", e)
                sleep(10)


    def grant_rights(self, number, rights, label):
        if number > len(self.chain_nodes):
            logger.error("Not enough Nodes. Requested %d had %d", number, len(self.chain_nodes))
            sys.exit(1)
        else:
            self.groups[label] = []
            for i in range(number):
                chain_node = self.chain_nodes.pop(0)
                for right in rights:
                    self.chain_rpc.grant(chain_node.getaddresses()[0], right)
                self.groups[label].append(chain_node)

    def issue_assets(self, asset_name, quantity, units):
        self.chain_rpc.issue(self.chain_rpc.getaddresses()[0], asset_name, quantity, units)

    def send_assets(self, sender, receipent, asset_name, quantity):
        logger.info("Send assets from %s to %s", sender, receipent)
        sender.sendasset(receipent.getaddresses()[0], asset_name, quantity)

    def send_assets_to_group(self, sender, receipent_group, asset_name, quantity):
        for member in self.groups[receipent_group]:
            self.send_assets(sender, member, asset_name, quantity)

    def revoke_rights(self, group, rights):
        for member in self.groups[group]:
            for right in rights:
                self.chain_rpc.revoke(member.getaddresses()[0], right)


if __name__ == '__main__':
    orchestrator = ScenarioOrchestrator()
    while True:
        sleep(1000000)  # So Docker will not stop container
