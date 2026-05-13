#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:30:59 2026

@author: joachim
"""

import json
import urllib.request
import urllib.parse

params = urllib.parse.urlencode({
    "latitude": 33.64054,
    "longitude": -117.83891,
    "current": "apparent_temperature,precipitation_probability,relative_humidity_2m",
})
endpoint = f"https://api.open-meteo.com/v1/forecast?{params}"

with urllib.request.urlopen(endpoint) as resp:
    data = json.loads(resp.read().decode("utf-8"))

print(data['current']['relative_humidity_2m'])