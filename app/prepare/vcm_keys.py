import json, logging
from app import config, crypto

"""
Create VCM (Vote Casting Machine) keys.
"""
def generate():
    logging.info("Reading vote casting machines from %s file" % config.VCM_FILE)

    with open(config.VCM_FILE) as json_file:
        vcms = json.load(json_file)

        for vcm in vcms:
            logging.info("Generating key pair for #%s VCM (Vote Casting Machine) in %s" %(vcm["id"], vcm["location"]))

            private_key, public_key = crypto.generate_key_pair()

            private_key_serialized = crypto.serialize_private_key(private_key)
            public_key_serialized = crypto.serialize_public_key(public_key)

            crypto.write_key_pair(config.VCM_KEYS_FOLDER, vcm["id"], private_key_serialized, public_key_serialized)

            logging.info("%s and %s.pub files are created" %(vcm["id"], vcm["id"]))
