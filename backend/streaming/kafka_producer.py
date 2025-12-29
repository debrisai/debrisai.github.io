
import os
import json
import datetime
from confluent_kafka import Producer

# Environment Variables
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_API_KEY = os.environ.get("KAFKA_API_KEY")
KAFKA_API_SECRET = os.environ.get("KAFKA_API_SECRET")

class KafkaProducer:
    def __init__(self):
        """
        Initializes the Kafka producer with credentials from environment variables.
        """
        conf = {
            "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": KAFKA_API_KEY,
            "sasl.password": KAFKA_API_SECRET,
        }
        self.producer = Producer(conf)

    def produce_event(self, topic, event_type, data):
        """
        Produces a standardized event to the specified Kafka topic.
        """
        event = {
            "event_type": event_type,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            **data,
        }
        self.producer.produce(topic, json.dumps(event).encode("utf-8"))
        self.producer.flush()
