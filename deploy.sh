#!/bin/bash

echo "🚀 Preparing AI Research Paper Generator for Railway Deployment"
echo "=============================================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: AI Research Paper Generator"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if all required files exist
echo "🔍 Checking required files..."

required_files=(
    "flask_app.py"
    "AImodel.py"
    "requirements.txt"
    "Procfile"
    "railway.json"
    "templates/index.html"
    "static/css/style.css"
    "static/js/script.js"
)

missing_files=()

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ All required files are present"
else
    echo "❌ Missing files:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "📝 Please create .env file with:"
    echo "   GOOGLE_API_KEY=your_google_api_key_here"
    echo ""
fi

echo "🎯 Ready for Railway deployment!"
echo ""
echo "Next steps:"
echo "1. Upload this folder to GitHub"
echo "2. Go to railway.app"
echo "3. Connect your GitHub repository"
echo "4. Add GOOGLE_API_KEY environment variable"
echo "5. Deploy!"
echo ""
echo "📖 See RAILWAY_DEPLOYMENT.md for detailed instructions"
