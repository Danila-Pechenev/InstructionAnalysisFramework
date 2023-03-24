#!/bin/bash
set -eou pipefail
#
# This is a script for collecting data from iso-image
# Run it from InstructionAnalysisFramework folder
# Usage:
# ./data_collection/local_iso_collection.sh <path_to_iso_file> <table_path> [optional: <objdump_command>
# (default: objdump)]
#
trap 'fusermount -q -u "$root" || true; rm -r -f "$root"' EXIT

objdump_command="${3:-objdump}"
root=$(mktemp -d)
fuseiso "$1" "$root"
python data_collection/data_collection.py scan-folder -o "$objdump_command" -d "$root" -r "$2"
fusermount -u "$root"
rmdir "$root"