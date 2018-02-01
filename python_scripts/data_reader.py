import logging
import subprocess
from configparser import ConfigParser
import time
import json
import yaml
from typing import Tuple

from websocket import create_connection, WebSocket
from Savoir import Savoir


def setup_logging():
    pass


def read_user_and_password() -> Tuple[str, str]:
    conf_string = '[conf]\n' + open('/root/.multichain/bpchain/multichain.conf').read()
    parser = ConfigParser()
    parser.read_string(conf_string)
    return parser.get('conf', 'rpcuser'), parser.get('conf', 'rpcpassword')


def read_rpc_port() -> str:
    conf_string = '[conf]\n' + open('/root/.multichain/multichain.conf').read()
    parser = ConfigParser()
    parser.read_string(conf_string)
    return parser.get('conf','rpcport')


def connect_to_multichain():
    user, password = read_user_and_password()
    rpc_host = 'localhost'
    rpc_port = read_rpc_port()
    chain_name = 'bpchain'
    rpc_api = Savoir(user, password, rpc_host, rpc_port, chain_name)
    return rpc_api


def get_node_data(rpc_api):
    difficulty = float(rpc_api.getmininginfo()['difficulty'])
    hashespersec = int(rpc_api.getmininginfo()['hashespersec'])
    is_mining = 0 if hashespersec == 0 else 1  # TODO: replace with 'correct' request
    print('############################')
    print(difficulty, hashespersec, is_mining)
    print('############################')
    #TODO: calculate blocktime by getting time between last blocks
    return {'chain': 'multichain', 'hostId': -1, 'hashrate': hashespersec, 'gasPrice': -1,
                 'avgDifficulty': difficulty, 'avgBlocktime': -1,
                 'isMining': is_mining}

def create_web_socket() -> WebSocket:
    uri = yaml.safe_load(open('config.yml'))
    timeout_in_seconds = 10
    web_socket = create_connection(
        uri['networking']['socketProtocol'] +
        uri['networking']['socketAdress'],
        timeout_in_seconds
    )
    logging.critical({'message': 'Connection established'})
    return web_socket


def send_data(node_data):
    try:
        web_socket = create_web_socket()
        web_socket.send(json.dumps(node_data))
        print('Sent\nReceiving...')
        result = web_socket.recv()
        print('Received ', result)
        logging.critical({'message': result})
        web_socket.close()
    # Not nice, but works for now.
    # pylint: disable=broad-except
    except Exception as exception:
        print('Exception occurred during sending: ')
        print(exception)
        logging.critical({'message': exception})


def provide_data_every(n_seconds, rpc_api):
    while True:
        time.sleep(n_seconds)
        try:
            node_data = get_node_data(rpc_api)
            send_data(node_data)
        # pylint: disable=broad-except
        except Exception as exception:
            print('During providing Data an error occurred: ', exception)
            logging.critical({'message': exception})


def main():
    time.sleep(10)  # sleep so we hopefully mine a block. TODO: replace with safe implementation
    send_period = 10
    rpc_api = connect_to_multichain()
    setup_logging()
    provide_data_every(send_period, rpc_api)


if __name__ == '__main__':
    main()
