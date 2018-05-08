"""Collect and send data to the api-server."""

import json
import os
import time
from configparser import ConfigParser
from typing import Tuple
from statistics import mean
from time import sleep

import yaml
from Savoir import Savoir
from websocket import create_connection, WebSocket

from ..project_logger import set_up_logging


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


def get_node_data(chain_node, last_block_number, hostname):
    difficulty = float(chain_node.getmininginfo()['difficulty'])
    hashespersec = int(chain_node.getmininginfo()['hashespersec'])
    is_mining = 0 if hashespersec == 0 else 1  # TODO: replace with 'correct' request
    avg_blocksize = calculate_avg_blocksize(chain_node, last_block_number)
    avg_blocktime, new_last_block_number = calculate_avg_blocktime(chain_node, last_block_number)
    return {'target': hostname, 'chainName': 'multichain', 'hostId': chain_node.getaddresses()[0],
            'hashrate': hashespersec, 'blockSize': avg_blocksize,
            'avgDifficulty': difficulty, 'avgBlocktime': avg_blocktime,
            'isMining': is_mining}, new_last_block_number


def calculate_avg_blocksize(chain_node, last_block_number) -> float:
    newest_block_number = chain_node.getblockchaininfo()['blocks']
    if last_block_number < newest_block_number:
        sizes = [chain_node.getblock(str(block_number))['size'] for block_number in
                 range(last_block_number, newest_block_number + 1)]
        return mean(sizes)
    else:
        if last_block_number == 0:
            return 0
        LOG.info('No new blocks using last available block size')
        return chain_node.getblock(str(last_block_number))['size']


def calculate_avg_blocktime(chain_node, last_block_number) -> Tuple[float, int]:
    newest_block_number = chain_node.getblockchaininfo()['blocks']
    newest_unix_time = time.time()
    if last_block_number < newest_block_number:
        old_unix_time = chain_node.getblock(str(last_block_number))['time']
        delta_blocks = newest_block_number - last_block_number
    else:
        if last_block_number == 0:
            return 0, 0
        old_unix_time = chain_node.getblock(str(last_block_number - 1))['time']
        delta_blocks = 1
    delta_time = newest_unix_time - old_unix_time
    return delta_time / delta_blocks, newest_block_number


def connect_to_server() -> WebSocket:
    uri = yaml.safe_load(open('/python_sources/data_acquisition/config.yml'))
    timeout_in_seconds = 10
    web_socket = create_connection(
        uri['networking']['socketProtocol'] +
        uri['networking']['socketAddress'],
        timeout_in_seconds
    )
    return web_socket


def send_data(node_data):
    try:
        ws_connection = connect_to_server()
        ws_connection.send(json.dumps(node_data))
        ws_connection.recv()
        ws_connection.close()
    # Not nice, but works for now.
    # pylint: disable=broad-except
    except Exception as exception:
        LOG.critical(exception)


def provide_data_every(n_seconds, rpc_api, hostname):
    last_block_number = 0
    while True:
        try:
            time.sleep(n_seconds)
            node_data, last_block_number = get_node_data(rpc_api, last_block_number, hostname)
            LOG.info(node_data)
            send_data(node_data)
        # pylint: disable=broad-except
        except Exception as exception:
            LOG.error(exception)


def main():
    hostname = os.environ["TARGET_HOSTNAME"]
    time.sleep(15)  # sleep so we hopefully mine a block. TODO: replace with safe
    # implementation
    send_period = 15
    rpc_api = connect_to_multichain()
    provide_data_every(send_period, rpc_api, hostname)


if __name__ == '__main__':
    sleep(300000)
    LOG = set_up_logging(__name__)
    main()
