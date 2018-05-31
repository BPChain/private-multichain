"""I collect data from multichain and send it to the server"""
import sys
from time import sleep

import yaml
from statistics_reader.sender import Sender

from python_sources.data_acquisition.multichian_adapter import MultichainAdapter


def main():
    is_miner = sys.argv[1] if len(sys.argv) > 1 else '1'
    uri = yaml.safe_load(open('/python_sources/data_acquisition/config.yml'))
    server_address = uri['serverAddress']
    Sender(server_address, 'multichaind', 'multichain', MultichainAdapter(is_miner))


if __name__ == '__main__':
    sleep(20)
    main()
