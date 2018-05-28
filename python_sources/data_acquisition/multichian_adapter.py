from typing import Tuple, List

from statistics_reader.block import Block
from statistics_reader.blockchain_adapter import BlockchainAdapter

from python_sources.data_acquisition.multichain_connector import connect_to_multichain


class MultichainAdapter(BlockchainAdapter):
    def __init__(self, is_miner):
        super().__init__(is_miner)
        self.rpc_client = connect_to_multichain()

    def fetch_newest_block_number(self) -> int:
        return self.rpc_client.getblockchaininfo()['blocks']

    def fetch_block_with(self, number: int):
        return self.rpc_client.getblock(str(number))

    def make_block_from(self, raw_block: dict) -> Block:
        return Block(raw_block['difficulty'], raw_block['tx'],
                     raw_block['time'], raw_block['size'])

    def hashrate(self) -> int:
        return int(self.rpc_client.getmininginfo()['hashespersec'])

    def is_mining(self) -> int:
        if self.is_miner == '0':
            return 0
        return 0 if self.hashrate() == 0 else 1

    def host_id(self):
        return self.rpc_client.getaddresses()[0]
