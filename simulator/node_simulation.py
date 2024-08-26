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

class NodeSimulation:
    def __init__(self, simulation_id, node_id, start_time, end_time, status):
        self.simulation_id = simulation_id
        self.node_id = node_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.queue = queue.Queue()

    def run(self):
        while True:
            item = self.queue.get()
            if item == "start":
                self.start_simulation()
            elif item == "stop":
                self.stop_simulation()
            self.queue.task_done()

    def start_simulation(self):
        # Start the simulation on the node
        print(f"Starting simulation on node {self.node_id}...")
        time.sleep(5)
        print(f"Simulation on node {self.node_id} started.")

    def stop_simulation(self):
        # Stop the simulation on the node
        print(f"Stopping simulation on node {self.node_id}...")
        time.sleep(5)
        print(f"Simulation on node {self.node_id} stopped.")

def main():
    node_simulation = NodeSimulation(1, 1, time.time(), time.time() + 3600, "running")
    thread = threading.Thread(target=node_simulation.run)
    thread.daemon = True
    thread.start()

    node_simulation.queue.put("start")
    time.sleep(10)
    node_simulation.queue.put("stop")

if __name__ == "__main__":
    main()
