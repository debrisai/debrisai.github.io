
import os
import time
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from api import vertex_inference, verifier_model, decision_logic
from streaming import kafka_producer

# Environment Variables
PORT = int(os.environ.get("PORT", 8080))
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC")

# Initialize Flask App
app = Flask(__name__)

# Initialize Kafka Producer
kafka_conn = kafka_producer.KafkaProducer()

@app.route("/analyze-image", methods=["POST"])
def analyze_image():
    """
    Accepts an image file, sends it to Gemini for analysis,
    verifies the result, and publishes an event to Kafka.
    """
    start_time = time.time()

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # 1. Get Gemini Response
        gemini_response, confidence = vertex_inference.analyze_image(file)

        # 2. Verification Layer
        final_response = decision_logic.decide_and_reprompt(gemini_response, confidence, file)

        # 3. Publish to Kafka
        latency_ms = int((time.time() - start_time) * 1000)
        kafka_conn.produce_event(
            KAFKA_TOPIC,
            "image_analysis",
            {
                "latency_ms": latency_ms,
                "confidence_score": confidence,
                "response": final_response,
            },
        )
        
        # 4. Add safety disclaimer
        final_response["disclaimer"] = "This is guidance only, not engineering certification. Always consult a qualified professional for structural applications."

        return jsonify(final_response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/chat", methods=["POST"])
def chat():
    """
    Accepts a text query, gets a response from Gemini,
    and publishes an event to Kafka.
    """
    start_time = time.time()
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    try:
        # 1. Get Gemini Response
        chat_response = vertex_inference.send_chat_message(data["query"])

        # 2. Publish to Kafka
        latency_ms = int((time.time() - start_time) * 1000)
        kafka_conn.produce_event(
            KAFKA_TOPIC,
            "chat",
            {
                "latency_ms": latency_ms,
                "query": data["query"],
                "response": chat_response,
            },
        )
        
        # 3. Add safety disclaimer
        final_response = {
            "response": chat_response,
            "disclaimer": "This is guidance only, not engineering certification. Always consult a qualified professional for structural applications."
        }

        return jsonify(final_response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
