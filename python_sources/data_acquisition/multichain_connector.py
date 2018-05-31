"""Connect to rpc server of multichain node"""

from configparser import ConfigParser
from typing import Tuple

from Savoir import Savoir


def read_user_and_password() -> Tuple[str, str]:
    conf_string = '[conf]\n' + open('/root/.multichain/bpchain/multichain.conf').read()
    parser = ConfigParser()
    parser.read_string(conf_string)
    return parser.get('conf', 'rpcuser'), parser.get('conf', 'rpcpassword')


def read_rpc_port() -> str:
    conf_string = '[conf]\n' + open('/root/.multichain/multichain.conf').read()
    parser = ConfigParser()
    parser.read_string(conf_string)
    return parser.get('conf', 'rpcport')


def connect_to_multichain() -> Savoir:
    user, password = read_user_and_password()
    rpc_host = 'localhost'
    rpc_port = read_rpc_port()
    chain_name = 'bpchain'
    chain_node = Savoir(user, password, rpc_host, rpc_port, chain_name)
    return chain_node
