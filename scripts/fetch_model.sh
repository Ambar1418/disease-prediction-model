#!/usr/bin/env bash
set -e

# Usage: ./scripts/fetch_model.sh <dest_path> <model_url>
DEST_PATH="$1"
MODEL_URL="$2"

if [ -z "$DEST_PATH" ] || [ -z "$MODEL_URL" ]; then
  echo "Usage: $0 <dest_path> <model_url>"
  exit 1
fi

if [ -f "$DEST_PATH" ]; then
  echo "Model already exists at $DEST_PATH - skipping download."
  exit 0
fi

mkdir -p "$(dirname "$DEST_PATH")"

echo "Downloading model from $MODEL_URL to $DEST_PATH"
# Use curl with retries
curl -fSL --retry 3 --retry-delay 5 "$MODEL_URL" -o "$DEST_PATH"

if [ $? -ne 0 ]; then
  echo "Failed to download model from $MODEL_URL"
  exit 2
fi

echo "Model downloaded successfully."
