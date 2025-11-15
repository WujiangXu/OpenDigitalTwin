#!/bin/bash

# English Teaching Assistant - Quick Start Script
# This script makes it easy to launch the voice-enabled English teaching assistant

echo "============================================================"
echo "🎓 English Teaching Assistant"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Check if .env file exists
if [ ! -f "config/.env" ]; then
    echo "⚠️  Warning: config/.env not found!"
    echo "   Please copy config/.env.example to config/.env"
    echo "   and add your OPENAI_API_KEY"
    echo ""
    echo "   Run: cp config/.env.example config/.env"
    echo "        nano config/.env"
    exit 1
fi

# Check if OpenAI API key is set
if ! grep -q "OPENAI_API_KEY=sk-" config/.env; then
    echo "⚠️  Warning: OPENAI_API_KEY not set in config/.env"
    echo "   Please add your OpenAI API key to config/.env"
    exit 1
fi

# Launch the English teaching assistant
echo "🚀 Launching English Teaching Assistant..."
echo ""

python3 main.py voice-chat "$@"
