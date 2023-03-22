#!/bin/bash
#
# This is a script for collecting data from iso-image
# Run it from InstructionAnalysisFramework folder
# Usage: ./data_collection/local_iso_collection.sh <path_to_iso_file> <table_path>
#
root=$(uuidgen)
sudo mkdir "$root"
sudo mount "$1" "$root" -o loop
python data_collection/data_collection.py scan-folder -d "$root" -r "$2"
sudo umount "$root"
sudo rmdir "$root"