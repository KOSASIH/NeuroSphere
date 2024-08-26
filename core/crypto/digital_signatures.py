import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes

class DigitalSignatures:
    def __init__(self):
        pass

    def generate_rsa_keypair(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def sign(self, private_key, data):
        signer = private_key.signer(
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        signature = signer.sign(data)
        return signature

    def verify(self, public_key, data, signature):
        verifier = public_key.verifier(
            signature,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        verifier.verify(data)

# Example usage:
digital_signatures = DigitalSignatures()
private_key, public_key = digital_signatures.generate_rsa_keypair()
data = b'Hello, World!'
signature = digital_signatures.sign(private_key, data)
digital_signatures.verify(public_key, data, signature)
