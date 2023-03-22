#!/bin/bash
#
# This is a script for collecting data from iso-image
# Run it from InstructionAnalysisFramework folder
# Usage: ./from_iso <path_to_image> <table_path>
#
root="$1"_$(uuidgen)
sudo mkdir "$root"
sudo mount "$1" "$root" -o loop
python data_collection/data_collection.py scan-folder -d "$root" -r "$2"
sudo umount "$root"
sudo rmdir "$root"