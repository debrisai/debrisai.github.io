# main.py - minimal FastAPI inference service (placeholder)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import random

app = FastAPI()

class InferenceRequest(BaseModel):
    image_url: str

@app.post("/run_inference")
def run_inference(req: InferenceRequest):
    # placeholder implementation - replace with model inference
    if not req.image_url:
        raise HTTPException(status_code=400, detail="image_url required")

    # Mocked response structure
    segments = [
        {"id": "seg1", "bbox": [10, 20, 100, 120], "mask_url": None}
    ]
    materials = [{"id": "seg1", "material": "concrete", "confidence": 0.93}]
    fit_score = round(random.uniform(0.0, 1.0), 2)
    reuse_suggestions = [
        {"title": "Garden paving block", "materials_needed": ["concrete pieces"], "effort": "low"}
    ]

    return {
        "segments": segments,
        "materials": materials,
        "fit_score": fit_score,
        "reuse_suggestions": reuse_suggestions,
        "inference_time_ms": 120
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
