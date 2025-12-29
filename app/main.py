
import os
from flask import Flask, request, jsonify
from vertexai.preview.generative_models import GenerativeModel, Part
import json
from kafka_producer import KafkaProducer
from verification_model import VerificationModel

app = Flask(__name__)

# Environment variables
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC")
KAFKA_API_KEY = os.environ.get("KAFKA_API_KEY")
KAFKA_API_SECRET = os.environ.get("KAFKA_API_SECRET")

# Initialize models and producer
gemini_model = GenerativeModel("gemini-pro-vision")
verification_model = VerificationModel()
kafka_producer = KafkaProducer(
    KAFKA_BOOTSTRAP_SERVERS, KAFKA_API_KEY, KAFKA_API_SECRET
)


@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    """
    Analyzes an image of construction rubble and returns a JSON object with the analysis results.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["image"]
    image_bytes = image_file.read()

    # Primary inference with Gemini Vision
    image_part = Part.from_data(image_bytes, mime_type="image/jpeg")
    prompt = """
    Analyze the provided image of construction debris and classify the primary material.
    Return a single JSON object with the following keys:
    - "material": "concrete | wood | metal | unknown"
    - "reuse_score": 0.0-1.0 (float)
    - "confidence": 0.0-1.0 (float)
    - "safety_class": "safe | caution | discard"
    - "notes": "A short explanation of the reasoning for the classification and scores."
    """
    response = gemini_model.generate_content([image_part, prompt])
    gemini_result = json.loads(response.text)

    # Secondary verification
    verifier_result = verification_model.verify(image_bytes)

    # Conservative, safety-first decision logic
    final_result = gemini_result.copy()
    if (
        verifier_result["confidence"] < 0.80
        or verifier_result["material"] != gemini_result["material"]
    ):
        final_result["safety_class"] = "discard"
        final_result["reuse_score"] = 0.0
        final_result["notes"] = (
            "Verification failed. Downgrading to conservative 'discard' classification. "
            + gemini_result["notes"]
        )

    # Publish to Kafka
    kafka_producer.produce(KAFKA_TOPIC, final_result)

    return jsonify(final_result)


@app.route("/chat", methods=["POST"])
def chat():
    """
    (Not implemented in this version)
    """
    return jsonify({"message": "Chat functionality not yet implemented."})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
