#!/usr/bin/env bash
# Remove background from a photo or a folder of photos using rembg.
#
# Usage:
#   ./remove-bg.sh input.jpg                 -> input.no-bg.png
#   ./remove-bg.sh input.jpg output.png
#   ./remove-bg.sh input_folder output_folder
#
# Model can be overridden: MODEL=u2net ./remove-bg.sh input.jpg
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMBG="$SCRIPT_DIR/.venv/bin/rembg"
MODEL="${MODEL:-birefnet-general}"

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <input file or folder> [output file or folder]" >&2
    exit 1
fi

input="$1"

# -dc decontaminates edge pixels: removes background color fringing
# while keeping the soft anti-aliased edge
if [[ -d "$input" ]]; then
    output="${2:-${input%/}_no_bg}"
    mkdir -p "$output"
    "$REMBG" p -m "$MODEL" -dc "$input" "$output"
elif [[ -f "$input" ]]; then
    output="${2:-${input%.*}.no-bg.png}"
    "$REMBG" i -m "$MODEL" -dc "$input" "$output"
else
    echo "Error: '$input' is not a file or folder" >&2
    exit 1
fi

echo "Done -> $output"
