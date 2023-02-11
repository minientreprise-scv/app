#!/bin/bash

echo "Compiling project files..."
python3 -m py_compile bin/production.py

echo "Moving compiled file to project root..."

mv bin/__pycache__/$(ls bin/__pycache__) serve.pyc


echo "Finished, execute serve.pyc to run in development mode"