from pathlib import Path


def file_path(value):
    path = Path(value)
    if not (path.exists() and path.is_file()):
        raise ValueError(f"File not found: {path}")
    return path
