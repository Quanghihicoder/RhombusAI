#!/bin/bash

# Get the absolute path of the current directory
BASE_DIR=$(pwd)

# Change directory to frontend and install npm packages
cd "$BASE_DIR/frontend"
npm install

# Change back to root directory
cd "$BASE_DIR"

# Change directory to backend and set up virtual environment
cd "$BASE_DIR/backend"
python3 -m venv venv  # Use python3 instead of python
source venv/bin/activate  # Activate venv
pip install -r requirements.txt
deactivate  # Deactivate venv

# Change back to root directory
cd "$BASE_DIR"

# Open a new terminal for frontend
osascript -e "tell application \"Terminal\" to do script \"cd \\\"$BASE_DIR/frontend\\\" && npm start\""

# Open another new terminal for backend
osascript -e "tell application \"Terminal\" to do script \"cd \\\"$BASE_DIR/backend\\\" && source venv/bin/activate && python manage.py runserver\""

echo "All setup complete. Use the opened terminals for running frontend and backend servers."

