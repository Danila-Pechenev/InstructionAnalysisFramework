import multiprocessing
import subprocess as sp
import pandas as pd
import click
import re

from file_generators import user_files_generator, non_recursive_file_generator, recursive_file_generator

OBJDUMP_ARGS = ["-d", "--no-show-raw-insn", "--no-addresses"]
INSTRUCTION_REGEX = r"^\s+([a-z]\S+)(\s+\S+)*$"


@click.command()
@click.option("--base-dir", "-d", default="/", help="Base directory for scanning.")
@click.option("--objdump-path", "-o", default="objdump", help="Path to objdump.")
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Recursively walk a directory tree (starting from base directory).",
)
@click.option(
    "--files",
    "-f",
    default=None,
    help="List of specific files on which program will be run. List items must not be separated by spaces, "
    "otherwise list must be placed in quotes.",
)
@click.argument("table-path")
def collect_data(base_dir: str, objdump_path: str, table_path: str, recursive: bool, files: str):
    """Walks through all the executable files in the folder and its subfolders and collect data"""
    n_cores = multiprocessing.cpu_count()
    if files:
        paths = parse_files(files)
        file_groups = [(list(user_files_generator(paths, n_cores, core)), objdump_path) for core in range(n_cores)]
    else:
        if recursive:
            file_groups = [
                (list(recursive_file_generator(base_dir, n_cores, core)), objdump_path) for core in range(n_cores)
            ]
        else:
            file_groups = [
                (list(non_recursive_file_generator(base_dir, n_cores, core)), objdump_path) for core in range(n_cores)
            ]

    with multiprocessing.Pool() as pool:
        dfs = pool.starmap(scan, file_groups)

    df = pd.concat(dfs, ignore_index=True).fillna(0)
    if len(df) != 0:
        col = df.pop("filename")
        df = df.astype(int)
        df.insert(0, "filename", col)

    df.to_csv(table_path, index=False)


def parse_files(files: str) -> list[str]:
    return [file.strip().strip("\"'") for file in files[1:-1].split(",")]


def run_objdump(path_to_elf: str, objdump_path: str) -> str:
    completed_process = sp.run([objdump_path, *OBJDUMP_ARGS, path_to_elf], capture_output=True)
    completed_process.check_returncode()
    return completed_process.stdout.decode("utf-8")


def get_elf_instructions(assembly_listing: str) -> dict[str, int]:
    instructions_count = dict()
    for line in assembly_listing.splitlines():
        matched = re.match(INSTRUCTION_REGEX, line)
        if matched:
            instruction = matched.group(1)
            if instruction not in instructions_count:
                instructions_count[instruction] = 1
            else:
                instructions_count[instruction] += 1

    return instructions_count


def scan(generator, objdump_path: str) -> pd.DataFrame:
    data = []
    for file in generator:
        try:
            assembly_listing = run_objdump(file, objdump_path)
            instructions_data = get_elf_instructions(assembly_listing)
            instructions_data["filename"] = file
            data.append(instructions_data)
        except sp.CalledProcessError:
            pass

    df = pd.DataFrame(data).fillna(0)
    if len(data) != 0:
        col = df.pop("filename")
        df = df.astype(int)
        df.insert(0, "filename", col)

    return df


if __name__ == "__main__":
    collect_data()
