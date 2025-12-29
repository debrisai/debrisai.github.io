# Vertex AI Endpoint for Debris AI

This document explains how the Debris AI backend uses Vertex AI for its core functionality.

## Gemini Pro Vision

The backend uses the `gemini-pro-vision` model for image analysis. This multimodal model can process both image and text inputs, making it ideal for the Debris AI use case.

### Prompting Strategy

The initial prompt sent to Gemini is designed to elicit a structured JSON response. This allows for easy parsing and handling of the model's output.

### Verification and Re-prompting

To ensure the reliability of the analysis, a verification layer is implemented. If the confidence score returned by Gemini is below a certain threshold (e.g., 80%), the system automatically re-prompts the model with a stricter, more conservative set of instructions. This helps to mitigate the risk of providing inaccurate or unsafe reuse suggestions.

## Gemini Pro

The backend uses the `gemini-pro` model for the chat functionality. This model is well-suited for conversational interactions and can provide helpful information about construction debris, reuse, and safety.

## Service Account Authentication

The backend authenticates with the Vertex AI API using the Cloud Run service account. This is a secure and recommended practice that avoids the need for hardcoded credentials or JSON key files.
