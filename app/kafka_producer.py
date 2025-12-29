from confluent_kafka import Producer
import json


class KafkaProducer:
    def __init__(self, bootstrap_servers, api_key, api_secret):
        """
        Initializes the Kafka producer.
        """
        conf = {
            "bootstrap.servers": bootstrap_servers,
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "sasl.username": api_key,
            "sasl.password": api_secret,
        }
        self.producer = Producer(conf)

    def produce(self, topic, message):
        """
        Sends a message to a Kafka topic.
        """
        self.producer.produce(topic, json.dumps(message).encode("utf-8"))
        self.producer.flush()
