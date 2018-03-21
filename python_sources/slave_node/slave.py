"""I send my multichain username and password to a master node so he can control my local
multichan instance """
import rpyc
from ..data_acquisition.data_acquisition import read_user_and_password, read_rpc_port


class SlaveService(rpyc.Service):
    # Do not use __init__ because of rpyc-library

    def on_connect(self):
        print("New Connection")

    def on_disconnect(self):
        print("Connection closed")

    def exposed_get_credentials(self):
        user, password = read_user_and_password()
        return user, password, read_rpc_port()


if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer

    SERVER = ThreadedServer(SlaveService, port=60000)
    print("start slave")
    SERVER.start()
