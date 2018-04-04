"""I send my multichain username and password to a master node so he can control my local
multichan instance """
from time import sleep

import rpyc

from ..data_acquisition.data_acquisition import read_user_and_password, read_rpc_port
from ..project_logger import set_up_logging

LOG = set_up_logging(__name__)

def get_credentials():
    user, password = read_user_and_password()
    return user, password, read_rpc_port()


if __name__ == '__main__':
    connection = rpyc.connect("privatemultichain_masternode_1", 60000)
    user, password = read_user_and_password()
    rpc_port = read_rpc_port()
    chainnode = connection.root.set_chainnodes(user, password, rpc_port)
    while True:
        sleep(20)
    connection.root.close(chainnode)
