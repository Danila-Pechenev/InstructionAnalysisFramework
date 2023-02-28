import multiprocessing
import subprocess as sp
import pandas as pd
import click
import os
import re

OBJDUMP_ARGS = ["-d", "--no-show-raw-insn", "--no-addresses"]
INSTRUCTION_REGEX = r"^\s+([a-z]\S+)(\s+\S+)*$"


@click.command()
@click.option('--base-dir', default='/', help='base directory for scanning')
@click.option('--objdump-path', default="objdump", help='path to objdump')
@click.argument('table-path')
def collect_data(base_dir: str, objdump_path: str, table_path: str):
    """Walks through all the executable files in the folder and its subfolders and collect data"""
    n_cores = multiprocessing.cpu_count()
    with multiprocessing.Pool() as pool:
        dfs = pool.starmap(scan,
                           [(list(file_generator(base_dir, n_cores, core)), objdump_path) for core in range(n_cores)])

    df = pd.concat(dfs, ignore_index=True).fillna(0)
    if len(df) != 0:
        col = df.pop("filename")
        df = df.astype(int)
        df.insert(0, "filename", col)

    df.to_csv(table_path, index=False)


def run_objdump(path_to_elf: str, objdump_path: str) -> str:
    completed_process = sp.run([objdump_path, *OBJDUMP_ARGS, path_to_elf], capture_output=True)
    completed_process.check_returncode()
    return completed_process.stdout.decode("utf-8")


def file_generator(base_dir: str, n_cores: int, core: int):
    count = -1
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            count += 1
            if count % n_cores == core:
                if file_path.startswith("/bin/"):
                    print(file_path)
                yield file_path


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
        except:
            pass

    df = pd.DataFrame(data).fillna(0)
    if len(data) != 0:
        col = df.pop("filename")
        df = df.astype(int)
        df.insert(0, "filename", col)

    return df


if __name__ == '__main__':
    collect_data()
