import os, glob, json
import config, crypto, blockchain

class Miner:
    """
    This class is simple abstract class
    just for showing responsibility of miner
    in the blockchain network.

    It just simulates miners' behavior,
    validates votes and saves.
    """

    blockchain = blockchain.Blockchain()

    def __init__(self, id):
        self._votes = []
        self.id = id
        self.private_key = crypto.load_private_key_file(config.MINER_KEYS_FOLDER, str(self.id))

    """
    Add a vote to waiting list.

    :param self: self class
    :param vote: vote data
    """
    def add_vote(self, vote):
        vote["header"]["hash_of_proof"] = crypto.sha256(
            json.dumps(vote["content"]["proof"], sort_keys=True)
        )

        self.validate_vote(vote)
        self.check_casted_vote(vote)

        self._votes.append(vote)

        if len(self._votes) >= config.BLOCKCHAIN_BLOCK_VOTE_LIMIT:
            self.blockchain.add_block({
                "content": self._votes,
                "header": {
                    "signature": crypto.sign(json.dumps(self._votes, sort_keys=True), self.private_key),
                    "miner_id": self.id
                }
            })

            self._votes = []

    """
    Validate a vote.

    :param self: self class
    :param vote: vote dictionary
    """
    def validate_vote(self, vote):
        genesis_block = self.blockchain.get_block(0)

        # check proof
        proofs = genesis_block["content"]["electronic_ballot_proofs"]

        if not vote["header"]["hash_of_proof"] in proofs:
            raise Exception("Invalid proof")

        # check VCM
        vcm_id = vote["header"]["vcm_id"]
        vcm_public_key = genesis_block["content"]["vcms"][vcm_id]["public_key"].encode('ascii')

        crypto.verify(vote["header"]["signature"], json.dumps(vote["content"], sort_keys=True), crypto.load_public_key(vcm_public_key))

    """
    Check if a vote is already casted.
    This can/should be done with different and efficient structures in a real instance.
    This can be done on tallying process, if it won't be done in blockchain network.

    :param self: self class
    :param vote: vote dictionary
    """
    def check_casted_vote(self, vote):
        blocks = self.blockchain.get_blocks()
        blocks = blocks[1:]
        blocks.append({
            "content": self._votes
        })

        for block in blocks:
            for vote_in_block in block["content"]:
                if vote_in_block["header"]["hash_of_proof"] == vote["header"]["hash_of_proof"]:
                    raise Exception("This vote is already casted")

