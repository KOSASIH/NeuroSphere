import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, transactions, timestamp):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + self.previous_hash + str(self.transactions) + str(self.timestamp)
        return hashlib.sha256(data.encode()).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "timestamp": self.timestamp,
            "hash": self.hash
        }

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.transactions = []

    def create_genesis_block(self):
        return Block(0, "0", [], int(time.time()))

    def mine_block(self):
        if not self.transactions:
            return
        new_block = Block(len(self.chain), self.chain[-1].hash, self.transactions, int(time.time()))
        self.chain.append(new_block)
        self.transactions = []

    def add_transaction(self, sender, recipient, amount):
        tx = Transaction(sender, recipient, amount)
        self.transactions.append(tx)
        return tx

    def last_block(self):
        return self.chain[-1]
