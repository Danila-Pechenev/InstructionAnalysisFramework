#!/bin/bash
set -euo pipefail
#
# This is a script for collecting data from a disk image by a link to it
# Run it from InstructionAnalysisFramework folder
# Usage:
# ./data_collection/url_disk_image_collection.sh <link_to_disk_image> <table_path> [optional: <objdump_command>
# (default: objdump)]
#
function clean {
    if [ -z ${iso_file+x} ]; then
        rm -f -- "$disk_image"
    fi
}
trap clean EXIT

objdump_command="${3:-objdump}"
disk_image=$(mktemp imageXXX.iso)
wget -O "$disk_image" "$1"
./data_collection/local_disk_image_collection.sh "$disk_image" "$2" "$objdump_command"