#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:09:18 2026

@author: joachim
"""

import os
import json
import urllib.request
from pathlib import Path

def load_api_key(key_file: Path = Path()) -> str:
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_key:
        return env_key
    if key_file.is_file():
        return json.loads(key_file.read_text())["api_key"]
    else:
        raise FileNotFoundError(f"Key file not found: {key_file}")
    raise ValueError("GEMINI_API_KEY is not set and key file not found.")

API_KEY = load_api_key()

url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

# POST request to Gemini API
body = {
    "contents": [
        {"parts": [{"text": "Explain diffusion models in cognitive science in one sentence."}]}
    ]
}
body_bytes = json.dumps(body).encode("utf-8")


# POST request to Gemini API
req = urllib.request.Request(
    url,
    data=body_bytes,
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    },
    method="POST"
)


# POST request to Gemini API
with urllib.request.urlopen(req) as resp:
    response_data = json.loads(resp.read().decode("utf-8"))

text = response_data["candidates"][0]["content"]["parts"][0]["text"]
print(text)