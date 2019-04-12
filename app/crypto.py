import os, logging, base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
import config

logging.basicConfig(level=logging.INFO)

"""
Generate key pair with RSA algorithm.

return private_key and public_key objects
"""
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    public_key = private_key.public_key()

    return private_key, public_key

"""
Serialize private key.

:param private_key: private key to serialize
"""
def serialize_private_key(private_key):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

"""
Serialize public key.

:param public_key: public key to serialize
"""
def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

"""
Create a file with given content

:param folder: folder to write keys
:param name: name of output files
:param private_key: serialized private key
:param public_key: serialized public key
"""
def write_key_pair(folder, name, private_key, public_key):
    with open(os.path.join(folder, name), "w") as file:
        file.write(private_key)

    with open(os.path.join(folder, name + ".pub"), "w") as file:
        file.write(public_key)

"""
Load private key

:param key: key
"""
def load_private_key(key):
    return serialization.load_pem_private_key(
        key,
        password=None,
        backend=default_backend()
    )

"""
Load public key from

:param key: key
"""
def load_public_key(key):
    return serialization.load_pem_public_key(
        key,
        backend=default_backend()
    )

"""
Load private key from a file

:param folder: folder to key file
"""
def load_private_key_file(folder, name):
    with open(os.path.join(folder, name), "rb") as file:
        return load_private_key(file.read())

"""
Load public key from a file

:param folder: folder to key file
"""
def load_public_key_file(folder, name):
    with open(os.path.join(folder, name + ".pub"), "rb") as file:
        return load_public_key(file.read())

"""
Return random string base64 encoded

:param byte_length: byte length of random output
"""
def random_string(byte_length = 64):
    random_bytes = os.urandom(byte_length)
    return base64.b64encode(random_bytes)

"""
Return sha256 hash of the message base64 encoded

:param message: message
"""
def sha256(message):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(message)
    return base64.b64encode(digest.finalize())

"""
Encrypt given message with given public key and return base64 encoded

:param message: message
:param public_key: public_key
"""
def encrypt(message, public_key):
    encrypted_message = public_key.encrypt(
        message,
        # make RSA probabilistic with OAEP, random output is needed
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return base64.b64encode(encrypted_message)

"""
Decrypt given base64 encoded ciphertext with given private key

:param message: message
:param public_key: public_key
"""
def decrypt(ciphertext, private_key):
    ciphertext_decoded = base64.b64decode(ciphertext)

    return private_key.decrypt(
        ciphertext_decoded,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

"""
Sign given message with given private key and return base64 encoded

:param message: message
:param private_key: private_key
"""
def sign(message, private_key):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return base64.b64encode(signature)

"""
Verify given base64 encoded signature with given private key and message.
If not verified, throw cryptography.exceptions.InvalidSignature

:param signature: signature
:param message: message
:param public_key: public_key
"""
def verify(signature, message, public_key):
    return public_key.verify(
        base64.b64decode(signature),
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
