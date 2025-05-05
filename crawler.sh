#!/bin/bash

# Default values
DEFAULT_THREADS=10
DEFAULT_MB=10

# Read args or use defaults
THREADS=${1:-$DEFAULT_THREADS}
MAX_MB=${2:-$DEFAULT_MB}

echo "Running crawler with:"
echo "- Threads: $THREADS"
echo "- Max JSON file size: ${MAX_MB}MB"

if [ "$#" -gt 2 ]; then
  echo "Warning: Extra arguments detected and will be ignored."
fi

# Run the crawler
python3 crawler.py \
    --threads "$THREADS" \
    --max-size-mb "$MAX_MB"