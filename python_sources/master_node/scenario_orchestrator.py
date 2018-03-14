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


        number_slaves = 3
        print("Orchestrator is ready for connections")
        try:
            print("connectiong")
            self.connect_to_slaves(number_slaves)
            print('connected')
        except ConnectionRefusedError:
            self.connect_to_slaves(number_slaves)
        self.get_slave_addresses()
        self.grant_rights(1, ['receive','send'], 'Blubber')

    def connect_to_slaves(self, number_of_slaves):
        sleep(20)
        for number in range(1,number_of_slaves+1):
            connection = rpyc.connect("privatemultichain_slavenode_"+str(number), 60000)
            user, password, rpc_port = connection.root.get_credentials()
            chain_node = Savoir(user, password, "privatemultichain_slavenode_"+str(number), rpc_port, "bpchain")
            self.chain_nodes.append(chain_node)
            print("################ Add connection")

    def get_slave_addresses(self):
        for chain_node in self.chain_nodes:
            print("############## Address new")
            print(chain_node.getaddresses())

    def grant_rights(self, number, rights, label):
        if number > len(self.chain_nodes):
            print('Error not enough resources')
        else:
            self.groups[label] = []
            for i in range(number):
                for right in rights:
                    self.chain_rpc.grant(self.chain_nodes[i].getaddresses()[0], right)
                self.groups[label].append(self.chain_nodes.pop(0))



if __name__ == '__main__':
    orchestrator = ScenarioOrchestrator()
