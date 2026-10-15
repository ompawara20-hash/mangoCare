#!/usr/bin/env bash

echo "============================================="
echo " Starting MangoCare AI Full-Stack System"
echo "============================================="

if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Trap SIGINT to kill background backend on exit
trap 'kill $(jobs -p) 2>/dev/null' EXIT

echo "Launching Backend on http://127.0.0.1:8000..."
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 &

echo "Launching Frontend on http://localhost:5173..."
cd frontend
npm run dev
