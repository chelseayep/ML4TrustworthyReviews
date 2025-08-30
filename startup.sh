#!/bin/bash

# ML4TrustworthyReviews Startup Script
echo "Starting ML4TrustworthyReviews application..."

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

# Add /src to PYTHONPATH
export PYTHONPATH="${PROJECT_ROOT}/src:$PYTHONPATH"
echo "Added ${PROJECT_ROOT}/src to PYTHONPATH"

# Check if virtual environment exists, create if it doesn't
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating new virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found in project root"
    exit 1
fi

# Install/update requirements
echo "Installing requirements from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if streamlit app exists
if [ ! -f "streamlit/Main.py" ]; then
    echo "Error: streamlit/Main.py not found"
    exit 1
fi

# Launch Streamlit app
echo "Launching Streamlit application..."
echo "Access the app at: http://localhost:8501"
streamlit run streamlit/Main.py

# Keep the script running until user stops it
echo "Application stopped."