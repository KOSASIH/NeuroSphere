import os
import sys
import time
import threading
import queue
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend
from consensus import ConsensusAlgorithm

class TestConsensus:
    def __init__(self):
        self.consensus_algorithm = ConsensusAlgorithm()
        self.nodes = []
        self.transactions = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def run_consensus(self):
        # Run the consensus algorithm
        self.consensus_algorithm.run(self.nodes, self.transactions)

    def test_consensus(self):
        # Test the consensus algorithm
        self.add_node(Node("Node 1", "192.168.1.100", 8080))
        self.add_node(Node("Node 2", "192.168.1.101", 8081))
        self.add_node(Node("Node 3", "192.168.1.102", 8082))
        self.add_transaction(Transaction("Transaction 1", "Sender 1", "Receiver 1", 10.0))
        self.add_transaction(Transaction("Transaction 2", "Sender 2", "Receiver 2", 20.0))
        self.add_transaction(Transaction("Transaction 3", "Sender 3", "Receiver 3", 30.0))
        self.run_consensus()
        print("Consensus algorithm completed.")

class Node:
    def __init__(self, name, ip_address, port):
        self.name = name
        self.ip_address = ip_address
        self.port = port

class Transaction:
    def __init__(self, id, sender, receiver, amount):
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

class ConsensusAlgorithm:
    def __init__(self):
        self.nodes = []
        self.transactions = []
        self.blockchain = []

    def run(self, nodes, transactions):
        # Run the consensus algorithm
        self.nodes = nodes
        self.transactions = transactions
        self.create_block()
        self.broadcast_block()
        self.verify_block()

    def create_block(self):
        # Create a new block
        block = Block(self.transactions)
        self.blockchain.append(block)

    def broadcast_block(self):
        # Broadcast the block to all nodes
        for node in self.nodes:
            node.receive_block(self.blockchain[-1])

    def verify_block(self):
        # Verify the block
        for node in self.nodes:
            node.verify_block(self.blockchain[-1])

class Block:
    def __init__(self, transactions):
        self.transactions = transactions
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Calculate the hash of the block
        hash = hashlib.sha256()
        for transaction in self.transactions:
            hash.update(transaction.id.encode())
        return hash.hexdigest()

if __name__ == "__main__":
    test_consensus = TestConsensus()
    test_consensus.test_consensus()
