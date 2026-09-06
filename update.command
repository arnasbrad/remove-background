#!/usr/bin/env bash
# Double-click (macOS) or run in a terminal to update to the latest version.
cd "$(dirname "$0")"
git fetch origin && git pull --ff-only origin main && echo "Up to date." || echo "Update failed (see above)."
read -r -p "Press Enter to close."
