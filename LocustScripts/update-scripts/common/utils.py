import csv
import json
import random

import yaml


def load_data(path):
    if path.suffix == ".csv":
        return load_csv_data(path)
    if path.suffix == ".json":
        return load_json_data(path)
    if path.suffix == ".yaml":
        return load_yaml_data(path)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def load_csv_data(path, model=None):
    with path.open() as f:
        reader = csv.DictReader(f)
        data = list(reader)

    if model:
        return [model(**row) for row in data]
    return data


def load_yaml_data(path, model=None):
    with path.open() as f:
        data = yaml.safe_load(f)

    if model:
        return model(**data)
    return data


def load_json_data(path):
    with path.open() as f:
        return json.load(f)


class RandomItems:
    def __init__(self, items=None):
        self.items = list(items) if items else []
        random.shuffle(self.items)

    def set(self, items):
        self.items = list(items)
        random.shuffle(self.items)

    def get(self):
        return self.items.pop()
