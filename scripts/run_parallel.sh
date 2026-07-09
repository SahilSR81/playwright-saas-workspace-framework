#!/usr/bin/env bash
set -euo pipefail

WORKERS="${1:-auto}"
MARKER="${2:-}"

echo "=== Parallel Test Execution ==="
echo "Workers : $WORKERS"
echo "Marker  : ${MARKER:-none}"

ARGS=(-n "$WORKERS" -v --tb=short)

if [[ -n "$MARKER" ]]; then
    ARGS+=(-m "$MARKER")
fi

rm -rf reports/allure-results/*
rm -rf playwright/.auth/*

pytest "${ARGS[@]}"

echo ""
echo "=== Done ==="
