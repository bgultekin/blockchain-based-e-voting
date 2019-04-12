import json, logging
from app import config, crypto

"""
Create miner keys.
"""
def generate():
    logging.info("Reading miners from %s file" % config.MINERS_FILE)

    with open(config.MINERS_FILE) as json_file:
        miners = json.load(json_file)

        for miner in miners:
            logging.info("Generating key pair for #%s Miner (%s)" %(miner["id"], miner["citizen_id"]))

            private_key, public_key = crypto.generate_key_pair()

            private_key_serialized = crypto.serialize_private_key(private_key)
            public_key_serialized = crypto.serialize_public_key(public_key)

            crypto.write_key_pair(config.MINER_KEYS_FOLDER, miner["id"], private_key_serialized, public_key_serialized)

            logging.info("%s and %s.pub files are created" %(miner["id"], miner["id"]))
