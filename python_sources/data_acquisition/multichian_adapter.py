from typing import Tuple, List

from statistics_reader.block import Block
from statistics_reader.blockchain_adapter import BlockchainAdapter

from python_sources.data_acquisition.data_acquisition import connect_to_multichain


class MultichainAdapter(BlockchainAdapter):

    def hashrate(self) -> int:
        return int(self.rpc_client.getmininginfo()['hashespersec'])

    def is_mining(self) -> int:
        if not self.is_miner:
            return 0
        return 0 if self.hashrate() == 0 else 1

    def host_id(self):
        return self.rpc_client.getaddresses()[0]

    def new_blocks_and_previous(self) -> Tuple[List[Block], Block]:
        newest_block_number = self.rpc_client.getblockchaininfo()['blocks']
        raw_blocks = [self.rpc_client.getblock(str(number))
                       for number in range(self.previous_block_number, newest_block_number + 1)]

        def make_block_from(raw_block: dict):
            return Block(raw_block['difficulty'], raw_block['tx'],
                         raw_block['time'], raw_block['size'])

        blocks = [make_block_from(raw_block) for raw_block in raw_blocks]
        old_block = blocks[0]
        new_blocks = blocks[1:] if len(blocks) > 1 else []
        return new_blocks, old_block

    def __init__(self, is_miner):
        super().__init__(is_miner)
        self.rpc_client = connect_to_multichain()
        self.previous_block_number = 0
