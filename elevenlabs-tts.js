const fetch = require('node-fetch');

async function synthesizeVoice(text) {
  const VOICE_ID = 'your_voice_id'; // choose voice from ElevenLabs dashboard
  const resp = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${VOICE_ID}`, {
    method: 'POST',
    headers: {
      'xi-api-key': process.env.ELEVENLABS_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text })
  });
  if (!resp.ok) throw new Error('TTS failed');
  const audioBuffer = await resp.arrayBuffer();
  return `data:audio/mpeg;base64,${Buffer.from(audioBuffer).toString('base64')}`;
}
module.exports = { synthesizeVoice };
