# Debris AI Backend

This project provides a backend for the Debris AI application. It analyzes images of construction rubble to determine their reuse potential.

## Deployment on Google Cloud

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/debris-ai-backend.git
    cd debris-ai-backend
    ```

2.  **Set up a Google Cloud project:**
    *   Create a new project in the [Google Cloud Console](https://console.cloud.google.com/).
    *   Enable the Cloud Run, Cloud Storage, and Vertex AI APIs.
    *   Create a service account with the "Cloud Run Invoker", "Storage Object Admin", and "Vertex AI User" roles.
    *   Download the service account key as a JSON file and save it as `gcp-credentials.json` in the project root.

3.  **Configure Confluent Cloud:**
    *   Create a new Kafka cluster in [Confluent Cloud](https://confluent.cloud/).
    *   Create a new topic for the inference results.
    *   Generate API keys for the Kafka cluster.

4.  **Set up environment variables:**
    *   Create a `.env` file in the project root and add the following variables:
        ```
        GOOGLE_APPLICATION_CREDENTIALS=gcp-credentials.json
        KAFKA_BOOTSTRAP_SERVERS=<your-kafka-bootstrap-servers>
        KAFKA_API_KEY=<your-kafka-api-key>
        KAFKA_API_SECRET=<your-kafka-api-secret>
        KAFKA_TOPIC=<your-kafka-topic>
        ```

5.  **Build and deploy the Docker image:**
    *   Build the Docker image:
        ```bash
        docker build -t gcr.io/your-gcp-project-id/debris-ai-backend .
        ```
    *   Push the Docker image to Google Container Registry:
        ```bash
        docker push gcr.io/your-gcp-project-id/debris-ai-backend
        ```
    *   Deploy the image to Cloud Run:
        ```bash
        gcloud run deploy debris-ai-backend \
          --image gcr.io/your-gcp-project-id/debris-ai-backend \
          --platform managed \
          --region us-central1 \
          --allow-unauthenticated
        ```

## API Endpoints

*   `POST /analyze-image`: Accepts an image file and returns a JSON object with the analysis results.
*   `POST /chat`: (Not implemented in this version)

## Kafka Producer

The `kafka_producer.py` module sends the analysis results to a Kafka topic in Confluent Cloud.
