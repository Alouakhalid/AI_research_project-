#!/bin/bash

echo "🚀 Starting AI Research Paper Generator..."
echo "=========================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Creating .env file..."
    echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
    echo "📝 Please edit .env file and add your Google API key"
    echo "🔗 Get your API key from: https://aistudio.google.com/app/apikey"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Start the Flask application
echo "🌐 Starting Flask application..."
echo "🤖 Using Gemini 2.5 Flash model"
echo "📍 Open your browser and go to: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python3 flask_app.py
