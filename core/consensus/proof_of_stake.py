import hashlib
import random

class ProofOfWork:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def hash_function(self, block_number, nonce, transactions):
        return hashlib.sha256(f'{block_number}{nonce}{transactions}'.encode()).hexdigest()

    def validate_proof(self, block_number, nonce, transactions):
        hash = self.hash_function(block_number, nonce, transactions)
        return hash[:self.difficulty] == '0' * self.difficulty

    def find_proof(self, block_number, transactions):
        nonce = random.randint(0, 2**32)
        while not self.validate_proof(block_number, nonce, transactions):
            nonce += 1
        return nonce

class ProofOfStake:
    def __init__(self, validators, stake_weights):
        self.validators = validators
        self.stake_weights = stake_weights

    def select_validator(self):
        return random.choices(self.validators, weights=self.stake_weights)[0]

    def validate_block(self, block_number, transactions, validator):
        return hashlib.sha256(f'{block_number}{transactions}{validator}'.encode()).hexdigest()[:32] == validator

    def create_block(self, transactions):
        validator = self.select_validator()
        block_number = random.randint(0, 2**32)
        nonce = ProofOfWork(difficulty=4).find_proof(block_number, transactions)
        return {
            'block_number': block_number,
            'transactions': transactions,
            'validator': validator,
            'nonce': nonce
        }

# Example usage:
validators = [...]
stake_weights = [...]
proof_of_stake = ProofOfStake(validators, stake_weights)
block = proof_of_stake.create_block([...])
