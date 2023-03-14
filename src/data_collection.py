import multiprocessing
import subprocess as sp
import pandas as pd
import click
import os

from file_generators import user_files_generator, non_recursive_file_generator, recursive_file_generator

OBJDUMP_ARGS = ["-d", "--no-show-raw-insn", "--no-addresses"]
PREFIXES = ["lock", "repne", "repnz", "rep", "repe", "repz", "cs", "ss", "ds", "es", "fs", "gs"]
ALLOWED_SYMBOLS = "0123456789qazwsxedcrfvtgbyhnujmikolp"


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
@click.option(
    "--ignore-folders",
    "-i",
    default=None,
    help="List of folders which will be ignored during data collection.",
)
@click.argument("table-path")
def collect_data(
    base_dir: str,
    objdump_path: str,
    recursive: bool,
    files: str | None,
    ignore_folders: str | None,
    table_path: str,
):
    """Walks through files according to the passed parameters and
    collects data (number of occurrences of each instruction)."""
    if ignore_folders:
        ignore_folders = parse_paths(ignore_folders)
    else:
        ignore_folders = []
    n_cores = multiprocessing.cpu_count()
    if files:
        paths = parse_paths(files)
        file_groups = [(list(user_files_generator(paths, n_cores, core)), objdump_path) for core in range(n_cores)]
    else:
        if recursive:
            file_groups = [
                (list(recursive_file_generator(base_dir, n_cores, core, ignore_folders)), objdump_path)
                for core in range(n_cores)
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

        df.set_index("filename", inplace=True)
        df = df.loc[list(set(df.index))]
        df.insert(0, "filename", df.index)
        df = df.set_index(pd.Index(i for i in range(len(df))))

    df.to_csv(table_path, index=False)


def parse_paths(paths: str) -> list[str]:
    return [path.strip().strip("\"'") for path in paths[1:-1].split(",")]


def run_objdump(path_to_elf: str, objdump_path: str) -> str:
    completed_process = sp.run([objdump_path, *OBJDUMP_ARGS, path_to_elf], capture_output=True)
    completed_process.check_returncode()
    return completed_process.stdout.decode("utf-8")


def run_readlink(path_to_file: str) -> str:
    completed_process = sp.run(["readlink", "-f", path_to_file], capture_output=True)
    return completed_process.stdout.decode("utf-8").split(os.linesep)[0]


def instruction_predicate(word: str) -> bool:
    for letter in word:
        if letter not in ALLOWED_SYMBOLS:
            return False
    if word in PREFIXES:
        return False

    return True


def process_one_line(line: str) -> str | None:
    words = line.split()
    for word in words:
        if instruction_predicate(word):
            return word


def get_elf_instructions(assembly_listing: str) -> dict[str, int]:
    instructions_count = dict()
    for line in assembly_listing.splitlines():
        instruction = process_one_line(line)
        if not instruction:
            continue
        if instruction not in instructions_count:
            instructions_count[instruction] = 1
        else:
            instructions_count[instruction] += 1

    return instructions_count


def scan(generator, objdump_path: str) -> pd.DataFrame:
    data = []
    for file in generator:
        file = run_readlink(file)
        try:
            assembly_listing = run_objdump(file, objdump_path)
            instructions_data = get_elf_instructions(assembly_listing)
            instructions_data["filename"] = file
            data.append(instructions_data)
        except sp.CalledProcessError:
            pass

    df = pd.DataFrame(data).fillna(0)

    return df


if __name__ == "__main__":
    collect_data()
