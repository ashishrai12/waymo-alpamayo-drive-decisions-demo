#!/bin/bash
# Script to run tests and linters

echo "Running tests..."
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest tests/

echo "Running flake8..."
flake8 src/ tests/
