// index.js - minimal express Raindrop backend
const express = require('express');
const fetch = require('node-fetch');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json({ limit: '20mb' }));

// ENV: RAINDROP_SDK_KEY, RAINDROP_API_URL, ELEVENLABS_KEY
const RAINDROP_API = process.env.RAINDROP_API_URL || 'https://api.raindrop.local';
const RAINDROP_KEY = process.env.RAINDROP_SDK_KEY;

// helper to call Raindrop SmartInference
async function callInference(image_url) {
  const resp = await fetch(`${RAINDROP_API}/v1/infer`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${RAINDROP_KEY}` },
    body: JSON.stringify({ image_url })
  });
  return resp.json();
}

// endpoint used by frontend
app.post('/infer', async (req, res) => {
  try {
    const { image_url } = req.body;
    if (!image_url) return res.status(400).json({ error: 'image_url required' });

    // 1) call Raindrop SmartInference (this routes to Vultr endpoint set in manifest)
    const inference = await callInference(image_url);

    // 2) store metadata in SmartSQL via Raindrop API (simplified)
    await fetch(`${RAINDROP_API}/v1/smartsql/parts-index`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${RAINDROP_KEY}` },
      body: JSON.stringify({
        image_url,
        materials: inference.materials || [],
        segments: inference.segments || [],
        fit_score: inference.fit_score ?? 0,
        created_at: new Date().toISOString()
      })
    });

    // 3) return inference to frontend
    res.json(inference);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'inference error', details: err.message });
  }
});

const port = process.env.PORT || 8080;
app.listen(port, ()=> console.log(`Raindrop API listening on ${port}`));
