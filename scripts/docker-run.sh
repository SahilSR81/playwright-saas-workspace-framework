#!/bin/bash

set -e

echo "Building Docker image..."
docker compose build

echo "Running tests..."
docker compose up --abort-on-container-exit

echo "Tests complete. Check reports/ for Allure results."
