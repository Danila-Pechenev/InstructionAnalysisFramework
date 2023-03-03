import os


def user_files_generator(user_files: list[str], n_cores: int, core: int):
    count = -1
    for path in user_files:
        count += 1
        if count % n_cores == core:
            yield path


def non_recursive_file_generator(base_dir: str, n_cores: int, core: int):
    count = -1
    for path in os.listdir(base_dir):
        file_path = os.path.join(base_dir, path)
        if os.path.isfile(file_path):
            count += 1
            if count % n_cores == core:
                yield file_path


def recursive_file_generator(base_dir: str, n_cores: int, core: int):
    count = -1
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            count += 1
            if count % n_cores == core:
                yield file_path
