
import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

# Environment Variables
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_REGION = os.environ.get("GOOGLE_CLOUD_REGION")

# Initialize Vertex AI
vertexai.init(project=GOOGLE_CLOUD_PROJECT, location=GOOGLE_CLOUD_REGION)

# Load the Gemini Pro Vision model
vision_model = GenerativeModel("gemini-pro-vision")
chat_model = GenerativeModel("gemini-pro")

def analyze_image(image_file):
    """
    Sends an image to Gemini Pro Vision and returns the JSON response.
    """
    image_part = Part.from_data(image_file.read(), mime_type=image_file.mimetype)
    
    prompt = '''
    Analyze the provided image of construction debris.
    Identify the primary material (brick, concrete, metal, wood), its reuse feasibility (0-100),
    and provide safe, non-structural reuse suggestions.
    Respond with a JSON object containing:
    - "materials": [array of detected materials]
    - "reuse_feasibility_score": integer (0-100)
    - "reuse_suggestions": "string"
    - "confidence_score": float (0.0-1.0) - your confidence in this analysis.
    '''

    response = vision_model.generate_content([image_part, prompt])
    
    # Extract and parse the JSON response
    # This is a simplified extraction. In a real app, you'd add more robust error handling here.
    response_text = response.candidates[0].content.parts[0].text
    response_json = eval(response_text) # Using eval for simplicity, but json.loads is safer
    
    confidence = response_json.get("confidence_score", 0.0)
    
    return response_json, confidence

def send_chat_message(query):
    """
    Sends a text query to the Gemini Pro model.
    """
    response = chat_model.generate_content(query)
    return response.candidates[0].content.parts[0].text

def reprompt_with_stricter_instructions(image_file):
    """
    Re-prompts Gemini with a more conservative set of instructions.
    """
    image_part = Part.from_data(image_file.read(), mime_type=image_file.mimetype)
    
    strict_prompt = '''
    Analyze the provided image of construction debris with a high degree of caution.
    If you are not highly confident, default to a low reuse score and 'not reusable' suggestions.
    Identify the primary material (brick, concrete, metal, wood), its reuse feasibility (0-100),
    and provide safe, non-structural reuse suggestions.
    Respond with a JSON object containing:
    - "materials": [array of detected materials]
    - "reuse_feasibility_score": integer (0-100)
    - "reuse_suggestions": "string"
    - "confidence_score": float (0.0-1.0) - your confidence in this analysis.
    '''
    response = vision_model.generate_content([image_part, strict_prompt])
    response_text = response.candidates[0].content.parts[0].text
    response_json = eval(response_text) # Using eval for simplicity
    
    return response_json
