#!/bin/bash
set -euo pipefail
#
# This is a script for collecting data from a disk image
# Run it from InstructionAnalysisFramework folder
# Usage:
# ./data_collection/local_disk_image_collection.sh <path_to_disk_image> <table_path> [optional: <objdump_command>
# (default: objdump)]
#
function clean {
    if [ -z ${root+x} ]; then
        fusermount -qu -- "$root" || true
        rmdir -- "$root"
    fi
}
trap clean EXIT

objdump_command="${3:-objdump}"
root=$(mktemp -d)
fuseiso -- "$1" "$root"
python data_collection/data_collection.py scan-folder -o "$objdump_command" -d "$root" -r -- "$2"