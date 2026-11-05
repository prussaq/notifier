#!/usr/bin/env bash
set -e

APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$APP_ROOT"

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing project in editable mode..."
pip install -e .

echo "Installation completed successfully."
