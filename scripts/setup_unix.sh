#!/usr/bin/env bash
set -e

echo "============================================="
echo " MangoCare AI - Automated Setup (Unix/macOS)"
echo "============================================="

# 1. Create Python Virtual Environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# 2. Activate Virtual Environment
source venv/bin/activate

# 3. Install Python Dependencies
echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

# 4. Initialize Database
echo "Initializing SQLite database..."
python backend/scripts/initialize_database.py

# 5. Verify / Download Models
echo "Verifying vision model weights..."
python backend/scripts/download_model.py

# 6. Install Frontend Packages & Build
echo "Installing frontend dependencies..."
cd frontend
npm install
npm run build
cd ..

echo "============================================="
echo " Setup Completed Successfully!"
echo " Run 'bash ./scripts/run_unix.sh' to start."
echo "============================================="
