import rpyc
from time import sleep
from Savoir import Savoir


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
        self.connection_refs = []
        number_slaves = 1
        print("Orchestrator is ready for connections")
        try:
            self.connect_to_slaves(number_slaves)
        except ConnectionRefusedError:
            self.connect_to_slaves(number_slaves)
        self.get_slave_addresses()

    def connect_to_slaves(self, number_of_slaves):
        sleep(20)

        connection = rpyc.connect('slavenode', 60000)
        self.connection_refs.append(connection)

    def get_slave_addresses(self):
        for con in self.connection_refs:
            print(con.root.wallet_addresses())
            print(con.root.get_credentials())
            user, password, rpc_port = con.root.get_credentials()
            s = Savoir(user, password, "slavenode", rpc_port, "bpchain")
            print(s.getinfo())




if __name__ == '__main__':
    orchestrator = ScenarioOrchestrator()
