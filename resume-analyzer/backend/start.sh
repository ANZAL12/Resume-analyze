#!/bin/bash

# Exit on any error
set -e

# Go to frontend folder and build React app
cd ../frontend
npm install
npm run build

# Go back to backend root folder
cd ../backend

# Install backend dependencies
pip install -r requirements.txt

# Start FastAPI server on Render's assigned port (default to 8000 if PORT not set)
PORT=${PORT:-8000}
uvicorn main:app --host 0.0.0.0 --port $PORT
