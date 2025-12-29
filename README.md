# Debris AI

Debris AI is a hackathon project that analyzes images of construction debris to identify materials, estimate reuse feasibility, and provide safe, non-structural reuse suggestions.

## Project Structure

The project is organized into the following directories:

*   `frontend/`: Contains the user interface for the application.
*   `backend/`: Contains the core backend logic, including the API server, Vertex AI integration, and Kafka streaming.
*   `models/`: Contains a conceptual notebook for training a verifier model.
*   `deployment/`: Contains documentation for setting up the project on Google Cloud and Confluent Cloud.

## Backend

The backend is a Python Flask application designed to be deployed on Cloud Run. It exposes two endpoints:

*   `POST /analyze-image`: Accepts an image of construction debris, analyzes it using Gemini, and returns a JSON response with material identification, reuse feasibility, and reuse suggestions.
*   `POST /chat`: Accepts a text query and returns a response from Gemini.

The backend also integrates with Confluent Cloud to stream events for every request.

## Safety

Debris AI prioritizes safety by providing a disclaimer with every analysis and offering conservative, non-structural reuse suggestions. A verification layer is also in place to re-prompt the model with stricter instructions if the initial confidence score is low.

## Getting Started

To get started with the project, please refer to the documentation in the `deployment/` directory.
