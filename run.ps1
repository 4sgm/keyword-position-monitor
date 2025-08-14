# PowerShell script to set up and run the backend on Windows
# Create virtual environment if it doesn't exist
if (-Not (Test-Path ".venv")) {
    python -m venv .venv
}

# Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r backend/requirements.txt

# Run the server
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
