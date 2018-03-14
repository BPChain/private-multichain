import rpyc
from ..data_acquisition.data_acquisition import connect_to_multichain


class SlaveService(rpyc.Service):
    # Do not use __init__ because of rpyc-library

    def on_connect(self):
        self.chain_rpc = connect_to_multichain()
        print("New Connection")

    def on_disconnect(self):
        print("Connection closed")

    def exposed_wallet_addresses(self):
        return self.chain_rpc.getaddresses()

if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(SlaveService, port=60000)
    print("start slave")
    server.start()