#!/bin/bash

# Check if an argument was provided
if [ "$1" == "simple" ]; then
    echo "Running simplified dashboard (app2.py)..."
    streamlit run app2.py
else
    echo "Running full dashboard (app.py)..."
    streamlit run app.py
fi