import hashlib

class HashFunctions:
    def __init__(self):
        pass

    def sha256(self, data):
        return hashlib.sha256(data).digest()

    def sha512(self, data):
        return hashlib.sha512(data).digest()

    def blake2b(self, data):
        return hashlib.blake2b(data).digest()

    def keccak256(self, data):
        return hashlib.keccak_256(data).digest()

# Example usage:
hash_functions = HashFunctions()
data = b'Hello, World!'
sha256_hash = hash_functions.sha256(data)
sha512_hash = hash_functions.sha512(data)
blake2b_hash = hash_functions.blake2b(data)
keccak256_hash = hash_functions.keccak256(data)
