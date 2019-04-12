import json, logging, os
from colors import *
from app import config, crypto
from app.blockchain import Blockchain

logging.info("Tallying process is started")

bc = Blockchain()
blocks = bc.get_blocks()

genesis_block = blocks[0]
blocks = blocks[1:]

logging.info("Private key of the election is not private anymore")
election_private_key = crypto.load_private_key_file(config.ELECTION_KEYS_FOLDER, "election")

# read election data and count
with open(config.ELECTION_FILE) as json_file:
    election = json.load(json_file)

for sub_election_id, sub_election in election.iteritems():
    sub_election["results"] = {key: 0 for key in sub_election["candidates"]}

for block in blocks:
    for ballot in block["content"]:
        election_id = ballot["content"]["proof"]["election_id"]
        vote = crypto.decrypt(ballot["content"]["vote"], election_private_key)

        election[str(election_id)]["results"][vote] += 1

logging.info("Tallying process is completed")

# dump results
with open(os.path.join(config.OUTPUT_FOLDER, "results.json"), "w") as json_file:
    json.dump(election, json_file)

logging.info("Results are saved in %s folder" % config.OUTPUT_FOLDER)
logging.info("Results can be seen below\n\n")

# print it beautifully
for sub_election_id, sub_election in election.iteritems():
    print("-" * 70)
    print("| " + color(sub_election["name"] + " Results", fg="yellow").ljust(75) + " |")
    print("-" * 70)
    print("| " + color("Candidate", style="bold").ljust(38) + " | " + color("Vote Count", style="bold").ljust(41) + " |")
    print("-" * 70)

    for candidate, result in sub_election["results"].iteritems():
        print("| %s | %s |" % (candidate.ljust(30), str(result).ljust(33)))
        print("-" * 70)

    print("\n")