import rpyc
from time import sleep
from Savoir import Savoir
from ..data_acquisition.data_acquisition import connect_to_multichain

# addresses = []
#
#
# def get_master_address():
#     return str(master_rpc.getaddresses())[2:-2]
#
#
# def generate_assets(asset_name, quantity, units):
#     get_master_address()
#     master_rpc.issue(get_master_address(), asset_name, quantity, units)
#     print('Issue ' + str(quantity) + ' of asset ' + asset_name)
#
#
# def grant_send_permission(address):
#     master_rpc.grant(address, 'send')
#
#
# def grant_receive_permission(address):
#     master_rpc.grant(address, 'receive')


class ScenarioOrchestrator:
    def __init__(self):
        self.chain_nodes = []
        self.chain_rpc = connect_to_multichain()
        self.groups = {}
        number_slaves = 10
        print("Orchestrator is ready for connections")
        print("Starting to connect")
        self.connect_to_slaves(number_slaves)
        print('Connected all Slaves')
        self.get_slave_addresses()
        self.grant_rights(2, ['receive','send'], 'Blubber')
        self.issue_assets('a1', 100, 0.1)

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

    def get_slave_addresses(self):
        for chain_node in self.chain_nodes:
            print("############## new Address")
            print(chain_node.getaddresses())

    def grant_rights(self, number, rights, label):
        if number > len(self.chain_nodes):
            print('Error not enough resources')
        else:
            self.groups[label] = []
            for i in range(number):
                for right in rights:
                    chain_node = self.chain_nodes.pop(0)
                    self.chain_rpc.grant(chain_node.getaddresses()[0], right)
                    self.groups[label].append(chain_node)

    def issue_assets(self, asset_name, quantity, units):
        self.chain_rpc.issue(self.chain_rpc.getaddresses()[0], asset_name, quantity, units)
        print('i issued assets')



if __name__ == '__main__':
    orchestrator = ScenarioOrchestrator()
