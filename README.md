# OpenAI Image Analyzer

Analyzes images from URLs using OpenAI's Vision API.

## Setup

1. Install dependencies:
```bash
pip install openai loguru
```

2. Install 1Password CLI from https://1password.com/downloads/command-line

3. Create OpenAI API key in 1Password:
```bash
op item create --category="API Credential" --title="OpenAI API" api_key="sk-..."
```

## Usage

1. Put URLs in `USER-FILES/04.INPUT/images.txt` (one per line)
2. Run: `python image_analyzer.py`
3. Results appear in `USER-FILES/05.OUTPUT/{timestamp}/`

That's it. Under 300 lines, does exactly what's needed.
EOF < /dev/null