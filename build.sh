#!/usr/bin/env bash
# Build script for Render.com

set -o errexit

echo "=== AeroFleet Manager Build Script ==="

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python init_db.py || echo "⚠️  Database init failed (will retry on startup)"

echo "✓ Build completed!"
