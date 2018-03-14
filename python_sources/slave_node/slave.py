import rpyc
from ..data_acquisition.data_acquisition import connect_to_multichain, read_user_and_password, read_rpc_port


class SlaveService(rpyc.Service):
    # Do not use __init__ because of rpyc-library

    def on_connect(self):
        self.exposed_chain_rpc = connect_to_multichain()
        print("New Connection")


    def on_disconnect(self):
        print("Connection closed")

    def exposed_wallet_addresses(self):
        return self.exposed_chain_rpc.getaddresses()

    def exposed_get_chain_rpc(self):
        return self.exposed_chain_rpc

    def exposed_get_credentials(self):
        user, password =  read_user_and_password()
        return user, password, read_rpc_port()


if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    server = ThreadedServer(SlaveService, port=60000)
    print("start slave")
    server.start()