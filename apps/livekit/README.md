In root directory (vocode-core)
```commandline
python3.11 -m venv venv
source venv/bin/activate
poetry install
```

Fill in the .env file from .env.example

```commandline
cd apps/livekit
poetry install
poetry run python app.py dev
```

Setup livekit cli 

```commandline
brew install livekit-cli
lk cloud auth
```

To initiate a call:
change number in sipParticipant.json to the number you want to call
```commandline
lk sip participant create sipParticipant.json
```