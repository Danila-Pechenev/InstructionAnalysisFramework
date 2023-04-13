#!/bin/bash
set -euo pipefail

usage="Usage: $(basename "$0") [OPTIONS] -- IMAGE TABLE_PATH

Scans a disk image.

Options:
    -u       Download the disk image by given URL.
    -p TEXT  Partition of the disk image. Default: /dev/sda1
    -o TEXT  Objdump command. Default: objdump
    -a       Save archive with image (if it appears during operation).
    -i       Save disk image (if it appears during operation).
    -h       Show this message and exit.

Args:
    IMAGE       URL or path to the disk image (can be packed).
    TABLE_PATH  Output table path."

function clean {
    if [[ -v mountpoint ]]; then
      if [[ -v mountedby ]]; then
        if [[ $mountedby == "fuseiso" ]]; then
          fusermount -qu -- "$mountpoint" || true
        elif [[ $mountedby == "guestmount" ]]; then
          guestunmount -q -- "$mountpoint" || true
        fi
      fi
      rmdir -- "$mountpoint"
    fi

    if [[ -v archive_to_remove && ! -v save_archive ]]; then
      rm -f -- "$archive_to_remove"
    fi

    if [[ -v remove_image && ! -v save_image ]]; then
      rm -f -- "$image"
    fi
}
trap clean EXIT

partition="/dev/sda1"
objdump="objdump"

while getopts up:o:aih OPTION; do
  case "$OPTION" in
    u)
      byurl="def"
      ;;
    p)
      partition="$OPTARG"
      ;;
    o)
      objdump="$OPTARG"
      ;;
    a)
      save_archive="def"
      ;;
    i)
      save_image="def"
      ;;
    h)
      echo "$usage"
      exit 0
      ;;
    ?)
      echo "Run: $(basename "$0") -h"
      exit 1
      ;;
  esac
done
shift "$((OPTIND - 1))"

image="$1"
table_path="$2"

if [[ -v byurl ]]; then
  remove_image="def"
  wget -N -- "$image"
  image="$(basename "$image")"
fi

extension="${image##*.}"
if [[ $extension == "xz" || $extension == "7z" || $extension == "bz2" ]]; then
  remove_image="def"
  if [[ -v byurl ]]; then
    archive_to_remove="$image"
  fi
  if [[ $extension == "xz" ]]; then
    unxz -k -f -- "$image"
  elif [[ $extension == "7z" ]]; then
    7z x -y -- "$image"
  else
    bzip2 -d -f -- "$image"
  fi
  image="${image%.*}"
fi

mountpoint=$(mktemp -d)
extension="${image##*.}"
if [[ $extension == "iso" ]]; then
  mountedby="fuseiso"
  fuseiso -- "$image" "$mountpoint"
elif [[ $extension == "img" || $extension == "vmdk" ]]; then
  mountedby="guestmount"
  guestmount -a "$image" -m "$partition" -r -- "$mountpoint"
else
  echo "Unsupported disk image format."
  exit 2
fi

python data_collection/data_collection.py scan-folder -o "$objdump" -d "$mountpoint" -r -- "$table_path"