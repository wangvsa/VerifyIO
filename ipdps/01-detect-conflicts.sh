#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <base_directory>"
    exit 1
fi

BASE_DIR="$1"
DETECTOR="$RECORDER_INSTALL_PATH/bin/conflict-detector"

if [[ ! -f "$DETECTOR" ]]; then
    echo "$DETECTOR not found. Please make sure RECORDER_INSTALL_PATH is set properly"
    exit 1
fi

for dir in "$BASE_DIR"/*/; do
    if [ -d "$dir" ]; then
        echo "Perform conflict detection on $dir"
        $DETECTOR "$dir"
    fi
done
