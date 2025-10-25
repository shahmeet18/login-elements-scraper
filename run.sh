#!/bin/bash

# Run the FastAPI server with Uvicorn
python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000