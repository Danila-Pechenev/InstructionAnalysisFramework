#!/usr/bin/env python3
import subprocess as sp
import click
import json


@click.command()
@click.argument("json-file-path")
@click.argument("image-key")
@click.argument("table-path")
def scan_image(
    json_file_path: str,
    image_key: str,
    table_path: str,
):
    """Scans disk image in GitHub Actions (runs-on: ubuntu).
    Takes the path to the json-file, key of the image in it, and the path to the table to save."""
    with open(json_file_path, "r") as read_file:
        image_info = json.load(read_file)["disk-images"]
    url, objdump_package, objdump_command = None, None, None
    for item in image_info:
        if item["key"] == image_key:
            url = item["url"]
            objdump_package = item["objdump-package"]
            objdump_command = item["objdump-command"]
    if url is None:
        raise KeyError("No such key.")
    sp.run(["sudo", "apt-get", "install", "--yes", objdump_package], capture_output=False)
    sp.run(["./data_collection/url_disk_image_collection.sh", url, table_path, objdump_command], capture_output=False)


if __name__ == "__main__":
    scan_image()
