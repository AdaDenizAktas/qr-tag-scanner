import os

def file_exists(path: str) -> bool:
    return os.path.isfile(path)
