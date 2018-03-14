import rpyc
from time import sleep


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
        self.slaves = []
        number_slaves = 1
        self.connect_to_slaves(number_slaves)
        self.get_slave_addresses()

    def connect_to_slaves(self, number_of_slaves):
        sleep(20)
        slave = rpyc.connect("slavenode_1", 60000)
        self.slaves.append(slave.root)
        print(self.slaves)

    def get_slave_addresses(self):
        for slave in self.slaves:
            print(slave.wallet_addresses())


if __name__ == '__main__':
    orchestrator = ScenarioOrchestrator()
