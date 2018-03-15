import socket

import rpyc
from time import sleep
from Savoir import Savoir
from ..data_acquisition.data_acquisition import connect_to_multichain

class ScenarioOrchestrator:
    def __init__(self):
        self.chain_nodes = []
        self.chain_rpc = connect_to_multichain()
        self.groups = {}
        print("Orchestrator is ready for connections")
        print("Starting to connect")


    def connect_to_slaves(self, number_of_slaves):
        sleep(20)
        unconnected_ids = list(range(1, number_of_slaves+1))
        for slave_id in unconnected_ids:
            try:
                connection = rpyc.connect("privatemultichain_slavenode_"+str(slave_id), 60000)
                user, password, rpc_port = connection.root.get_credentials()
                chain_node = Savoir(user, password, "privatemultichain_slavenode_" + str(slave_id),
                                    rpc_port, "bpchain")
                self.chain_nodes.append(chain_node)
                unconnected_ids.remove(slave_id)
                print("################ Added connection to", slave_id)
            except ConnectionRefusedError:
                print("Could not connect to", slave_id, "retry later")
            except socket.gaierror:
                print("could not resolve name. removing id")
                unconnected_ids.remove(slave_id)


    def grant_rights(self, number, rights, label):
        if number > len(self.chain_nodes):
            print('Error not enough resources')
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
