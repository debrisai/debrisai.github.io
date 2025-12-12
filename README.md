# DebrisAI Backend Package (ready-to-deploy)

This archive contains the minimal backend and inference scaffold for DebrisAI:
- `raindrop.manifest.yaml` - Raindrop manifest (SmartBuckets, SmartSQL, SmartMemory, SmartInference)
- `server/` - Node.js Raindrop backend exposing `/infer`
- `inference/` - FastAPI inference service (placeholder) + Dockerfile
- `elevenlabs-tts.js` - example ElevenLabs TTS helper

## Quick start (local testing)
1. Inference service (local):
   ```
   cd inference
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   Test:
   ```
   curl -X POST http://localhost:8000/run_inference -H "Content-Type: application/json" -d '{"image_url":"https://example.com/test.jpg"}'
   ```

2. Raindrop backend (local):
   ```
   cd server
   npm install
   RAINDROP_API_URL=http://localhost:8000 RAINDROP_SDK_KEY=demo node index.js
   ```
   (Note: when deployed on Raindrop, use the platform's environment variables and endpoints.)

## Deploying
- Build & push inference Docker image, deploy to Vultr, set the public URL in `raindrop.manifest.yaml`.
- Deploy `raindrop.manifest.yaml` with Raindrop CLI: `raindrop deploy --manifest raindrop.manifest.yaml`
- Deploy the Node backend to Raindrop MCP (follow Raindrop MCP docs) or run as a service and configure CORS.

## Next steps
- Replace placeholder inference with your finetuned model (PyTorch/ONNX/Triton).
- Secure secrets (RAINDROP_SDK_KEY, ELEVENLABS_KEY) in Raindrop env or Vercel secrets.
- Connect Framer frontend to the Raindrop backend `/infer` endpoint.
