from colors import *
from app.prepare import *

"""
Preparation step for the election.
"""

print(color("Preparation process is started", fg="cyan"))
print(color("*", fg="gray") * 100)

print(color("Voter keys generation:", fg="yellow"))
print(color("-", fg="gray") * 100)

voter_keys.generate()

print(color("*", fg="gray") * 100)
print(color("Miners keys generation", fg="yellow"))
print(color("-", fg="gray") * 100)

miner_keys.generate()

print(color("*", fg="gray") * 100)
print(color("VCMs (vote casting machine) keys generation", fg="yellow"))
print(color("-", fg="gray") * 100)

vcm_keys.generate()

print(color("*", fg="gray") * 100)
print(color("Genesis block generation", fg="yellow"))
print(color("-", fg="gray") * 100)

genesis_block.generate()

print(color("*", fg="gray") * 100)
print(color("Preparation process is done", fg="cyan"))
