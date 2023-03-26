#!/bin/bash
set -euo pipefail
#
# This is a script for collecting data from iso image by a link to it
# Run it from InstructionAnalysisFramework folder
# Usage:
# ./data_collection/url_iso_collection.sh <link_to_iso_file> <table_path> [optional: <objdump_command>
# (default: objdump)]
#
function clean {
    if [ -z ${iso_file+x} ]; then
        rm -f -- "$iso_file"
    fi
}
trap clean EXIT

objdump_command="${3:-objdump}"
iso_file=$(mktemp imageXXX.iso)
wget -O "$iso_file" "$1"
./data_collection/local_iso_collection.sh "$iso_file" "$2" "$objdump_command"