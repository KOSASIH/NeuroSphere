import hashlib
import hmac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class QuantumResistant:
    def __init__(self, private_key):
        self.private_key = private_key

    def generate_public_key(self):
        private_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key = x25519.X25519PublicKey.from_private_key(self.private_key)
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.OpenSSH,
            format=serialization.PublicFormat.OpenSSH
        )
        return public_bytes

    def generate_shared_secret(self, peer_public_key):
        shared_secret = self.private_key.exchange(peer_public_key)
        return shared_secret

    def derive_symmetric_key(self, shared_secret, salt):
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            info=b'handshake data'
        ).derive(shared_secret)
        return derived_key

    def encrypt(self, plaintext, derived_key):
        encryptor = hmac.new(derived_key, plaintext, hashlib.sha256)
        ciphertext = encryptor.digest()
        return ciphertext

    def decrypt(self, ciphertext, derived_key):
        decryptor = hmac.new(derived_key, ciphertext, hashlib.sha256)
        plaintext = decryptor.digest()
        return plaintext

# Example usage:
private_key = x25519.X25519PrivateKey.generate()
quantum_resistant = QuantumResistant(private_key)
public_key = quantum_resistant.generate_public_key()
shared_secret = quantum_resistant.generate_shared_secret(peer_public_key)
derived_key = quantum_resistant.derive_symmetric_key(shared_secret, salt)
ciphertext = quantum_resistant.encrypt(plaintext, derived_key)
plaintext = quantum_resistant.decrypt(ciphertext, derived_key)
