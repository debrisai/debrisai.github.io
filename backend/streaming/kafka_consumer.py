
import os
from confluent_kafka import Consumer, KafkaError

# Environment Variables
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_API_KEY = os.environ.get("KAFKA_API_KEY")
KAFKA_API_SECRET = os.environ.get("KAFKA_API_SECRET")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC")

def consume_events():
    """
    Consumes and prints events from the Kafka topic.
    """
    conf = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "security.protocol": "SASL_SSL",
        "sasl.mechanisms": "PLAIN",
        "sasl.username": KAFKA_API_KEY,
        "sasl.password": KAFKA_API_SECRET,
        "group.id": "debris-ai-consumer-1",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(conf)
    consumer.subscribe([KAFKA_TOPIC])

    print(f"Subscribed to topic: {KAFKA_TOPIC}")

    try:
        while True:
            msg = consumer.poll(1.0) # Poll for new messages every second

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    continue
                else:
                    print(msg.error())
                    break

            print(f"Received message: {msg.value().decode('utf-8')}")

    except KeyboardInterrupt:
        pass
    finally:
        # Cleanly close the consumer
        consumer.close()

if __name__ == "__main__":
    consume_events()
