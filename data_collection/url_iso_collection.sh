#!/bin/bash
#
# This is a script for collecting data from iso-image by a link to it
# Run it from InstructionAnalysisFramework folder
# Usage: ./data_collection/url_iso_collection.sh <link_to_iso_file> <table_path>
#
iso_file=$(mktemp imageXXX.iso)
wget -O "$iso_file" "$1"
./data_collection/local_iso_collection.sh "$iso_file" "$2"
rm "$iso_file"