import os, glob, json, time
import config, crypto, blockchain, miner

class VCM:
    """
    This class is simple abstract class
    just for showing responsibility of
    VCM (Vote Casting Machine).

    It just simulates VCMs' behavior.
    """

    blockchain = blockchain.Blockchain()
    miner = miner.Miner(100)
    election_public_key = crypto.load_public_key_file(config.ELECTION_KEYS_FOLDER, "election")

    def __init__(self, id):
        self.id = id
        self.private_key = crypto.load_private_key_file(config.VCM_KEYS_FOLDER, str(self.id))
        self.genesis_block = self.blockchain.get_block(0)

    """
    Start the machine.

    :param self: self class
    """
    def start(self):
        while True:
            os.system("clear")

            print("Welcome to Voting Interface")

            voter_id = raw_input("Please enter your ID: ")

            print("Verifying election signature...")

            self._verify_genesis_block()

            print("Election signature verification is successful")
            print("Fetching your electronic ballots...")

            voter_decrypted_ballots = self._get_voter_ballots(voter_id)

            print("Time to vote...")

            # let user read output
            self._wait_and_clear(2)

            for ballot in voter_decrypted_ballots:
                election_id_to_vote = ballot["election_id"]
                election_to_vote = self.genesis_block["content"]["election"][str(election_id_to_vote)]

                print("=" * 50)
                print("Please make your choice for %s \n" % election_to_vote["name"])
                print("Canditates are below: \n")

                for index, candidate in enumerate(election_to_vote["candidates"], start=1):
                    print("%d) %s" % (index, candidate))

                while True:
                    candidate_index = raw_input("\nPlease enter your choice: ")
                    candidate_index = int(candidate_index)

                    if candidate_index > 0 and candidate_index <= len(election_to_vote["candidates"]):
                        chosen_candidate = election_to_vote["candidates"][candidate_index - 1]

                        self.miner.add_vote(
                            self._cast_vote(chosen_candidate, ballot)
                        )

                        print("\nYou have chosen %s to vote" % (chosen_candidate))
                        print("=" * 50)

                        self._wait_and_clear(1)

                        break
                    else:
                        print("Please enter a value between 1 and %d \n" % (len(election_to_vote["candidates"])))

            print("Thanks for voting!")
            print("Restarting...")

            self._wait_and_clear(3)

    """
    Verify genesis block.

    :param self: self class
    """
    def _verify_genesis_block(self):
        crypto.verify(self.genesis_block["header"]["signature"], json.dumps(self.genesis_block["content"], sort_keys=True), self.election_public_key)

    """
    Get given voter's ballots.

    :param self: self class
    :param voter_id: voter_id
    """
    def _get_voter_ballots(self, voter_id):
        voter_decrypted_ballots = []
        voter_private_key = crypto.load_private_key_file(config.VOTER_KEYS_FOLDER, voter_id)
        voter_ballots = self.genesis_block["content"]["encrypted_ballots"][voter_id]

        for ballot in voter_ballots:
            decrypted_ballot = crypto.decrypt(ballot, voter_private_key)
            voter_decrypted_ballots.append(json.loads(decrypted_ballot))

        return voter_decrypted_ballots

    """
    Cast a vote with given parameters and sign it.

    :param self: self class
    :param chosen_candidate: chosen candidate
    :param proof: ballot content
    """
    def _cast_vote(self, chosen_candidate, proof):
        content = {
            "proof": proof,
            "vote": crypto.encrypt(str(chosen_candidate), self.election_public_key)
        }

        return {
            "content": content,
            "header": {
                "signature": crypto.sign(json.dumps(content, sort_keys=True), self.private_key),
                "vcm_id": self.id
            }
        }

    """
    Wait given seconds and clear terminal.

    :param self: self class
    :param wait: wait
    """
    def _wait_and_clear(self, wait):
        time.sleep(wait)
        os.system("clear")
