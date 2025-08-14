"""
OpenAI Image Analyzer - Analyzes images from URLs using OpenAI Vision API.
Usage: python -m openai_image_analyzer
"""

import json
import yaml
import subprocess
import shutil
import os
import sys
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
from openai import OpenAI
from loguru import logger

# Get project root (2 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()

# Setup logging
log_path = PROJECT_ROOT / "USER-FILES" / "05.OUTPUT" / "image_analyzer.log"
logger.add(str(log_path), rotation="10 MB")

def get_api_key(item_name: str, field_name: str) -> str:
    """Get API key from 1Password CLI."""
    op_cli = shutil.which("op")
    if not op_cli:
        logger.error("1Password CLI not found. Install from: https://1password.com/downloads/command-line")
        sys.exit(1)
    
    # Check if authenticated
    try:
        subprocess.run([op_cli, "account", "get"], check=True, capture_output=True, timeout=10)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        logger.info("Authenticating with 1Password...")
        # Let user authenticate interactively
        result = subprocess.run([op_cli, "signin"], stdin=sys.stdin, stderr=sys.stderr, stdout=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logger.error("Failed to authenticate with 1Password")
            sys.exit(1)
        
        # Set session from output
        for line in result.stdout.strip().split("\n"):
            if line.startswith("export "):
                key, value = line.replace("export ", "").split("=", 1)
                os.environ[key] = value.strip('"')
    
    # Get the API key
    try:
        api_key = subprocess.check_output(
            [op_cli, "item", "get", item_name, "--field", field_name],
            text=True
        ).strip()
        return api_key
    except subprocess.CalledProcessError:
        logger.error(f"Could not get API key from 1Password item '{item_name}'")
        sys.exit(1)

def analyze_image(client: OpenAI, image_url: str, prompt: str, model: str, max_tokens: int, pricing_tier: str = "standard") -> dict:
    """Analyze a single image URL and return JSON response."""
    try:
        # Create payload for documentation
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ],
            "max_completion_tokens": max_tokens,
            "response_format": {"type": "json_object"}
        }
        
        # Add pricing tier to payload documentation
        if pricing_tier != "standard":
            payload["_pricing_tier"] = pricing_tier
        
        # Save payload to payload.md if debug mode is enabled
        if os.environ.get("DEBUG", "").lower() in ["true", "1", "yes"]:
            with open(PROJECT_ROOT / "payload.md", "w") as f:
                f.write("# OpenAI API Payload\n\n")
                f.write(f"**Pricing Tier:** {pricing_tier}\n\n")
                f.write("```json\n")
                f.write(json.dumps(payload, indent=2))
                f.write("\n```\n")
        
        # Set up extra headers for pricing tier
        extra_headers = {}
        if pricing_tier in ["batch", "flex", "priority"]:
            # OpenAI uses headers to control pricing tier
            extra_headers["openai-processing"] = pricing_tier
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]}
            ],
            max_completion_tokens=max_tokens,
            response_format={"type": "json_object"},
            extra_headers=extra_headers if extra_headers else None
        )
        content = response.choices[0].message.content
        if not content:
            logger.error(f"Empty response from API for {image_url}")
            return {"error": "Empty response from API"}
        return json.loads(content)
    except Exception as e:
        logger.error(f"Failed to analyze {image_url}: {e}")
        return {"error": str(e)}

def main():
    """Main processing function."""
    # Load config - try .yml first, then .json for backwards compatibility
    config_path_yml = PROJECT_ROOT / "USER-FILES" / "01.CONFIG" / "config.yml"
    config_path_json = PROJECT_ROOT / "USER-FILES" / "01.CONFIG" / "config.json"
    
    if config_path_yml.exists():
        with open(config_path_yml) as f:
            config = yaml.safe_load(f)
    elif config_path_json.exists():
        with open(config_path_json) as f:
            config = json.load(f)
    else:
        logger.error("Config file not found at USER-FILES/01.CONFIG/config.yml or config.json")
        sys.exit(1)
    
    # Load prompt
    prompt_path = PROJECT_ROOT / "USER-FILES" / "01.CONFIG" / "system_prompt.txt"
    if not prompt_path.exists():
        logger.error(f"System prompt file not found at {prompt_path}")
        sys.exit(1)
    
    with open(prompt_path) as f:
        prompt = f.read().strip()
    
    # Get API key from 1Password
    api_key = get_api_key(config["1password_item"], config["1password_field"])
    client = OpenAI(api_key=api_key)
    
    # Get pricing tier from config (default to standard if not specified)
    pricing_tier = config.get("pricing_tier", "standard")
    logger.info(f"Using pricing tier: {pricing_tier}")
    
    # Create output directory
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    output_dir = PROJECT_ROOT / "USER-FILES" / "05.OUTPUT" / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process all input files
    input_dir = PROJECT_ROOT / "USER-FILES" / "04.INPUT"
    input_files = list(input_dir.glob("*.txt"))
    
    if not input_files:
        logger.info("No input files found in USER-FILES/04.INPUT/")
        return
    
    logger.info(f"Processing {len(input_files)} files...")
    
    for input_file in input_files:
        logger.info(f"Processing {input_file.name}")
        
        # Read URLs
        with open(input_file) as f:
            urls = [line.strip() for line in f if line.strip()]
        
        if not urls:
            logger.warning(f"No URLs found in {input_file.name}")
            continue
        
        # Process each URL
        for url in urls:
            logger.info(f"Analyzing: {url}")
            
            # Get filename from URL
            filename = Path(urlparse(url).path).stem or "unnamed"
            
            # Analyze image
            analysis = analyze_image(client, url, prompt, config["model"], config["max_tokens"], pricing_tier)
            
            # Save result directly from OpenAI
            result_file = output_dir / f"{filename}.json"
            with open(result_file, "w") as f:
                json.dump(analysis, f, indent=2)
            
            logger.info(f"Saved: {result_file}")
    
    logger.info(f"Processing complete! Results in: {output_dir}")

if __name__ == "__main__":
    main()