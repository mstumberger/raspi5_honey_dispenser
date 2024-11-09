#!/bin/bash
# Use a subshell to run the environment
(
    source venv/bin/activate
    # Run the Python script
    cd src
    python3 .
)