import json, logging, os
from app import config, crypto
from app.blockchain import Blockchain

"""
Create genesis block and include all needed
information into it.
"""
def generate():
    logging.info("Genesis block generation is started")

    # election keys
    election_private_key, election_public_key = crypto.generate_key_pair()
    election_private_key_serialized = crypto.serialize_private_key(election_private_key)
    election_public_key_serialized = crypto.serialize_public_key(election_public_key)

    crypto.write_key_pair(config.ELECTION_KEYS_FOLDER, "election", election_private_key_serialized, election_public_key_serialized)

    logging.info("Election key pair is generated")
    logging.info("Reading voters from voters.json file")

    electronic_ballot_proofs = []
    encrypted_ballots = {}

    # electronic ballots
    with open(config.VOTERS_FILE) as json_file:
        voters = json.load(json_file)

        for voter in voters:
            logging.info("Generating electronic ballots for %s, %s %s" %(voter["id"], voter["name"], voter["surname"]))
            voter_public_key = crypto.load_public_key_file(config.VOTER_KEYS_FOLDER, voter["id"])
            encrypted_ballots[voter["id"]] = []

            for sub_election in voter["eligible_for_voting"]:
                ballot_id = crypto.random_string()
                electronic_ballot = {
                    "ballot_id": ballot_id,
                    "election_id": sub_election
                }

                electronic_ballot_json = json.dumps(electronic_ballot)
                electronic_ballot_proof = crypto.sha256(electronic_ballot_json)
                electronic_ballot_encrypted = crypto.encrypt(electronic_ballot_json, voter_public_key)

                electronic_ballot_proofs.append(electronic_ballot_proof)
                encrypted_ballots[voter["id"]].append(electronic_ballot_encrypted)


    logging.info("Reading election data")

    # election data
    with open(config.ELECTION_FILE) as json_file:
        election = json.load(json_file)

    logging.info("Reading miners data and public keys")

    # miners data and public keys
    with open(config.MINERS_FILE) as json_file:
        miners_list = json.load(json_file)
        miners = {}

        for miner in miners_list:
            with open(os.path.join(config.MINER_KEYS_FOLDER, miner["id"] + ".pub"), "rb") as file:
                miners[miner["id"]] = {
                    "public_key": file.read(),
                    "citizen_id": miner["citizen_id"]
                }

    logging.info("Reading VCMs data and public keys")

    # vcm data and public keys
    with open(config.VCM_FILE) as json_file:
        vcms_list = json.load(json_file)
        vcms = {}

        for vcm in vcms_list:
            with open(os.path.join(config.VCM_KEYS_FOLDER, vcm["id"] + ".pub"), "rb") as file:
                vcms[vcm["id"]] = {
                    "public_key": file.read(),
                    "location": vcm["location"]
                }

    # creating the genesis block
    logging.info("Creating genesis block")

    genesis_block_content = {
        "encrypted_ballots": encrypted_ballots,
        "electronic_ballot_proofs": electronic_ballot_proofs,
        "election": election,
        "miners": miners,
        "vcms": vcms
    }

    logging.info("Signing genesis block")

    genesis_block = {
        "header": {
            "signature": crypto.sign(json.dumps(genesis_block_content, sort_keys=True), election_private_key)
        },
        "content": genesis_block_content
    }

    logging.info("Saving genesis block")

    bc = Blockchain()
    bc.purge()
    bc.add_block(genesis_block)

    logging.info("Genesis block generation is completed")
