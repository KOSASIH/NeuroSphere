import os
import sys
import time
import hashlib
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend

class TestCrypto:
    def __init__(self):
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()

    def generate_private_key(self):
        # Generate a private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        return private_key

    def generate_public_key(self):
        # Generate a public key
        public_key = self.private_key.public_key()
        return public_key

    def encrypt(self, message):
        # Encrypt a message
        encrypted_message = self.public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_message

    def decrypt(self, encrypted_message):
        # Decrypt a message
        decrypted_message = self.private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode()

    def sign(self, message):
        # Sign a message
        signature = self.private_key.sign(
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify(self, message, signature):
        # Verify a signature
        self.public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    def test_crypto(self):
        # Test the crypto functions
        message = "Hello, World!"
        encrypted_message = self.encrypt(message)
        print("Encrypted message:", encrypted_message)
        decrypted_message = self.decrypt(encrypted_message)
        print("Decrypted message:", decrypted_message)
        signature = self.sign(message)
        print("Signature:", signature)
        self.verify(message, signature)
        print("Verification successful!")

if __name__ == "__main__":
    test_crypto = TestCrypto()
    test_crypto.test_crypto()
