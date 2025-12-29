
from api import vertex_inference, verifier_model

def decide_and_reprompt(gemini_response, confidence, image_file):
    """
    Evaluates the confidence score from Gemini.
    If below threshold, it re-prompts with stricter instructions.
    """
    if confidence < verifier_model.CONFIDENCE_THRESHOLD:
        # Rewind the file pointer to re-read the image data
        image_file.seek(0)
        # Re-prompt Gemini with stricter instructions
        return vertex_inference.reprompt_with_stricter_instructions(image_file)
    else:
        return gemini_response
