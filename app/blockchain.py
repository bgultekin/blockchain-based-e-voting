import os, glob, json
import config, crypto

class Blockchain:
    """
    This class is simple abstract class
    just for showing responsibility of blockchain
    in the code and content of blocks.

    It just simulates blockchain behavior
    and saves given data to files.
    """

    def __init__(self):
        self._blocks = []
        block_files = self._list_block_files()

        for block_file in block_files:
            with open(block_file) as file:
                self._blocks.append(json.load(file))

    """
    Add a block to chain and create a file.

    :param self: self class
    :param block_content: block
    """
    def add_block(self, block):
        block_count = len(self._blocks)

        # if this is not the genesis_block
        # then we should validate it
        if (block_count > 0):
            self._validate_block(block)

        self._blocks.append(block)

        block_file_name = self._name_block(block_count)

        with open(os.path.join(config.BLOCKCHAIN_FOLDER, block_file_name), "w") as block_file:
            block_file.write(json.dumps(block, sort_keys=True))

    """
    Get a block content.

    :param self: self class
    :param index: index of the block

    :return: block as a dictionary
    """
    def get_block(self, index):
        return self._blocks[index]

    """
    Get all blocks.

    :param self: self class

    :return: blocks as a list
    """
    def get_blocks(self):
        return self._blocks

    """
    Get the last block content.

    :param self: self class

    :return: the last block as a dictionary
    """
    def get_last_block(self):
        last_index = len(self._blocks) - 1

        return self._blocks[last_index]

    """
    Clear database and delete all files.

    :param self: self class
    """
    def purge(self):
        block_files = self._list_block_files()
        self._blocks = []

        for block_file in block_files:
            os.remove(block_file)

    """
    List block files.

    :param self: self class

    :return: sorted files as a list
    """
    def _list_block_files(self):
        block_files = glob.glob(os.path.join(config.BLOCKCHAIN_FOLDER, "*.json"))

        return sorted(block_files)

    """
    Name a block.

    :param self: self class
    :param index: index of the block
    """
    def _name_block(self, index):
        return str(index) + '.json'

    """
    Validate a block.
    This is normally responsibility of miners.

    :param self: self class
    :param index: block
    """
    def _validate_block(self, block):
        miner_id = block["header"]["miner_id"]
        miner_public_key = self.get_block(0)["content"]["miners"][str(miner_id)]["public_key"].encode('ascii')

        crypto.verify(block["header"]["signature"], json.dumps(block["content"], sort_keys=True), crypto.load_public_key(miner_public_key))
