#!/bin/bash

echo "🚀 Setting up Mapping the Gay Guides Flask App..."
echo "================================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first:"
    echo "   Visit: https://nodejs.org/"
    echo "   Or use Homebrew: brew install node"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Build Tailwind CSS (production build, no watch mode)
echo "🎨 Building Tailwind CSS..."
npm run build-prod

# Initialize database
echo "🗄️  Initializing database..."
python3 init_db.py

echo ""
echo "🎉 Setup complete! You can now run:"
echo "   python3 app.py"
echo ""
echo "The main app will be available at: http://localhost:5001"
echo ""
echo "For development tools, run:"
echo "   cd utilities"
echo "   python utility_app.py"
echo "   (Available at: http://localhost:5002)"
