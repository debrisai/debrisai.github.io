# Confluent Cloud Setup for Debris AI

This document provides instructions for setting up a Confluent Cloud cluster and integrating it with the Debris AI backend.

## 1. Create a Confluent Cloud Cluster

1.  **Sign up for Confluent Cloud:** If you don't have an account, you can sign up for a free trial.
2.  **Create a new cluster:** Follow the Confluent Cloud documentation to create a new Kafka cluster.

## 2. Create a Kafka Topic

Create a new Kafka topic to be used for the Debris AI events. You can do this through the Confluent Cloud UI or using the Confluent CLI.

## 3. Generate API Credentials

1.  **Navigate to the API keys section:** In the Confluent Cloud UI, find the section for managing API keys.
2.  **Create a new API key:** Generate a new API key and secret. Make sure to save the key and secret in a secure location, as you will not be able to see the secret again.

## 4. Environment Variables

When deploying the Cloud Run service, set the following environment variables with your Confluent Cloud credentials and topic information:

*   `KAFKA_BOOTSTRAP_SERVERS`: Your Confluent Cloud bootstrap server URL.
*   `KAFKA_API_KEY`: Your Confluent Cloud API key.
*   `KAFKA_API_SECRET`: Your Confluent Cloud API secret.
*   `KAFKA_TOPIC`: The name of the Kafka topic you created.

These environment variables will be used by the `kafka_producer.py` and `kafka_consumer.py` modules to connect to your Confluent Cloud cluster.
