import os


def user_files_generator(user_files: list[str], n_cores: int, core: int):
    count = -1
    for file_path in user_files:
        count += 1
        if count % n_cores == core:
            yield file_path


def non_recursive_file_generator(base_dir: str, n_cores: int, core: int):
    count = -1
    for path in os.listdir(base_dir):
        file_path = os.path.join(base_dir, path)
        if os.path.isfile(file_path):
            count += 1
            if count % n_cores == core:
                yield file_path


def recursive_file_generator(base_dir: str, n_cores: int, core: int, ignore_folders: list[str]):
    count = -1
    for root, _, files in os.walk(base_dir):
        if is_ignored(root, ignore_folders):
            print(f"Ignored: {root}")
            continue
        for file in files:
            if "DataCollection" in root:
                print(root)
            file_path = os.path.join(root, file)
            count += 1
            if count % n_cores == core:
                yield file_path


def is_ignored(folder: str, ignore_folders: list[str]) -> bool:
    for ignored_folder in ignore_folders:
        if folder.startswith(ignored_folder):
            return True
    return False
