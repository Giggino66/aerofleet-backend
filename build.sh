#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
python init_db.py || echo "init_db warning - will retry on startup"
