import json, logging
from app import config, crypto

"""
Create voter keys.
"""
def generate():
    logging.info("Reading voters from %s file" % config.VOTERS_FILE)

    with open(config.VOTERS_FILE) as json_file:
        voters = json.load(json_file)

        for voter in voters:
            logging.info("Generating key pair for %s, %s %s" %(voter["id"], voter["name"], voter["surname"]))

            private_key, public_key = crypto.generate_key_pair()

            private_key_serialized = crypto.serialize_private_key(private_key)
            public_key_serialized = crypto.serialize_public_key(public_key)

            crypto.write_key_pair(config.VOTER_KEYS_FOLDER, voter["id"], private_key_serialized, public_key_serialized)

            logging.info("%s and %s.pub files are created" %(voter["id"], voter["id"]))
