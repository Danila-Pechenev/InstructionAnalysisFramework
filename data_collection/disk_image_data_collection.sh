#!/bin/bash
set -euo pipefail

usage="Usage: $(basename "$0") [OPTIONS] IMAGE TABLE_PATH

Scans a disk image.

Options:
    -u       Download the disk image by given URL.
    -p TEXT  Partition of the disk image. Default: /dev/sda1
    -o TEXT  Objdump command. Default: objdump
    -h       Show this message and exit.

Args:
    IMAGE       URL or path to the disk image.
    TABLE_PATH  Output table path."

partition="/dev/sda1"
objdump="objdump"

while getopts u:p:o:h: OPTION; do
  case "$OPTION" in
    u)
      byurl="byurl"
      ;;
    p)
      partition="$OPTARG"
      ;;
    o)
      objdump="$OPTARG"
      ;;
    h)
      echo "$usage"
      exit 0
      ;;
    ?)
      echo "Run: $(basename $0) -h"
      exit 1
      ;;
  esac
done
shift "$((OPTIND - 1))"

image="$1"
table_path="$2"

working_dir=$(mktemp -d)
cd "$working_dir"

if [ -z ${byurl+x} ]; then
  wget image
  image="$(basename image)"
fi

extension="${image##*.}"
