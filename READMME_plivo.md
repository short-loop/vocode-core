.env at `apps/telephony_app/.env`

```dotenv
BASE_URL=<ngrok_url>
PLIVO_AUTH_ID=<plivo_auth_id>
PLIVO_AUTH_TOKEN=<plivo_auth_token>
DEEPGRAM_API_KEY=<deepgram_api_key>
OPENAI_API_KEY=<openai_api_key>
ELEVENLABS_API_KEY=<elevenlabs_api_key>
```

```commandline
python3.11 -m venv venv
source venv/bin/activate
poetry install
cd apps/telephony_app
python test.py
```