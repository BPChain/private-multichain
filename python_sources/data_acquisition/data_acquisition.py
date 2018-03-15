import logging
from configparser import ConfigParser
import time
import json
import yaml
from typing import Tuple

from websocket import create_connection, WebSocket
from Savoir import Savoir


def setup_logging():
    # TODO: Implement
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
    return parser.get('conf', 'rpcport')


def connect_to_multichain() -> Savoir:
    user, password = read_user_and_password()
    rpc_host = 'localhost'
    rpc_port = read_rpc_port()
    chain_name = 'bpchain'
    chain_node = Savoir(user, password, rpc_host, rpc_port, chain_name)
    return chain_node


def get_node_data(chain_node, last_block_number):
    difficulty = float(chain_node.getmininginfo()['difficulty'])
    hashespersec = int(chain_node.getmininginfo()['hashespersec'])
    is_mining = 0 if hashespersec == 0 else 1  # TODO: replace with 'correct' request
    avg_blocktime, new_last_block_number = calculate_avg_blocktime(chain_node, last_block_number)
    logging.info(difficulty, hashespersec, is_mining, avg_blocktime)
    return {'chainName': 'multichain', 'hostId': chain_node.getaddresses()[0], 'hashrate':
        hashespersec,
            'gasPrice': -1,
            'avgDifficulty': difficulty, 'avgBlocktime': avg_blocktime,
            'isMining': is_mining}, new_last_block_number


def calculate_avg_blocktime(chain_node, last_block_number):
    newest_block_number = chain_node.getblockchaininfo()['blocks']
    newest_unix_time = time.time()
    if last_block_number < newest_block_number:
        old_unix_time = chain_node.getblock(str(last_block_number))['time']
        delta_blocks = newest_block_number - last_block_number
    else:
        if last_block_number == 0:
            return 0
        old_unix_time = chain_node.getblock(str(last_block_number - 1))['time']
        delta_blocks = 1
    delta_time = newest_unix_time-old_unix_time
    return delta_time/delta_blocks, newest_block_number


def connect_to_server() -> WebSocket:
    uri = yaml.safe_load(open('/python_sources/data_acquisition/config.yml'))
    timeout_in_seconds = 10
    web_socket = create_connection(
        uri['networking']['socketProtocol'] +
        uri['networking']['socketAddress'],
        timeout_in_seconds
    )
    logging.info({'message': 'Connection established'})
    return web_socket


def send_data(node_data):
    try:
        ws_connection = connect_to_server()
        ws_connection.send(json.dumps(node_data))
        result = ws_connection.recv()
        logging.critical({'message': result})
        ws_connection.close()
    # Not nice, but works for now.
    # pylint: disable=broad-except
    except Exception as exception:
        logging.critical({'message': exception})


def provide_data_every(n_seconds, rpc_api):
    last_block_number = 0
    while True:
        time.sleep(n_seconds)
        try:
            node_data, last_block_number = get_node_data(rpc_api, last_block_number)
            print(node_data)
            send_data(node_data)
        # pylint: disable=broad-except
        except Exception as exception:
            logging.critical({'message': exception})


def main():
    time.sleep(15)  # sleep so we hopefully mine a block. TODO: replace with safe implementation
    send_period = 10
    setup_logging()
    rpc_api = connect_to_multichain()
    #provide_data_every(send_period, rpc_api)


if __name__ == '__main__':
    main()
