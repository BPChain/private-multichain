import sys
from time import sleep

import yaml
from statistics_reader.blockchain_reader import BlockchainReader
from statistics_reader.sender import Sender

from python_sources.data_acquisition.multichian_adapter import MultichainAdapter


def main():
    is_miner = sys.argv[1] if len(sys.argv) > 1 else '1'
    uri = yaml.safe_load(open('/python_sources/data_acquisition/config.yml'))
    server_address = uri['networking']['socketProtocol'] + uri['networking']['socketAddress']
    Sender(server_address, 15, BlockchainReader('multichaind', 'multichain', MultichainAdapter(is_miner)))


if __name__ == '__main__':
    sleep(20)
    main()