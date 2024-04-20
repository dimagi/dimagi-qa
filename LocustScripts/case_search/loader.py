import pathlib

from case_search.models import QueryData
from common.utils import load_csv_data, load_data, load_yaml_data


def load_query_data(path):
    data = load_yaml_data(path)
    value_sets = []
    for value_set in data["value_sets"]:
        if "path" in value_set:
            value_sets.extend(load_value_set_from_reference(path, value_set))
        else:
            value_sets.append(value_set)

    return QueryData.model_validate({
        "value_sets": value_sets,
        "queries": data["queries"],
    })


def load_value_set_from_reference(source_path, reference):
    path_str = reference.pop("path")
    path = pathlib.Path(path_str)
    if not path.is_absolute():
        path = source_path.parent / path

    if not path.exists():
        raise ValueError(f"Value set file not found: {path}")

    _format = reference.pop("format")
    return {
        "csv": load_value_set_from_csv,
    }[_format](path, **reference)


def load_value_set_from_csv(path, name_template, type):
    """Load value sets from a CSV file.

    Args:
        path (Path): Path to the CSV file.
        name_template (str): Template for the value set name. Will be formaqted with each row.
        keys (list[str]): Keys for the value set.
    """
    data = load_csv_data(path)
    return [
        {
            "name": name_template.format(**row),
            "type": type,
            "values": row,
        }
        for row in data
    ]
