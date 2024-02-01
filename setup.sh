#!/bin/bash
python3 -m pip install -U discord.py
python3 -m venv bot-env
source bot-env/bin/activate
pip install -U discord.py
pip install requests os-sys logging python-dotenv
