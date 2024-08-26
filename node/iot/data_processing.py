import json
import logging
import os
import pandas as pd
from kafka import KafkaConsumer
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data processing class
class DataProcessing:
    def __init__(self, kafka_topic: str, model_path: str):
        self.kafka_topic = kafka_topic
        self.model_path = model_path
        self.consumer = KafkaConsumer(kafka_topic, bootstrap_servers=['kafka:9092'], group_id='data_processing')
        self.scaler = StandardScaler()
        self.model = load_model(model_path)

    def process_data(self):
        for message in self.consumer:
            data = json.loads(message.value)
            features = pd.DataFrame([data['features']])
            features_scaled = self.scaler.fit_transform(features)
            prediction = self.model.predict(features_scaled)
            self.send_prediction(prediction)

    def send_prediction(self, prediction: np.ndarray):
        logger.info(f'Sent prediction to IoT Hub: {prediction}')

if __name__ == '__main__':
    kafka_topic = os.environ['KAFKA_TOPIC']
    model_path = os.environ['MODEL_PATH']
    data_processing = DataProcessing(kafka_topic, model_path)
    data_processing.process_data()
