import os
import logging
from kafka import KafkaProducer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka producer class
class KafkaProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=[bootstrap_servers])

    def send_message(self, message: str):
        try:
            self.producer.send(self.topic, value=message.encode('utf-8'))
            logger.info(f'Sent message to Kafka topic {self.topic}: {message}')
        except Exception as e:
            logger.error(f'Error sending message to Kafka topic {self.topic}: {e}')

if __name__ == '__main__':
    bootstrap_servers = os.environ['KAFKA_BOOTSTRAP_SERVERS']
    topic = os.environ['KAFKA_TOPIC']
    kafka_producer = KafkaProducer(bootstrap_servers, topic)
    kafka_producer.send_message('Hello, Kafka!')
