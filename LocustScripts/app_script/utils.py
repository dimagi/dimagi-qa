def merge_dicts(dict1, dict2):
    assert isinstance(dict1, dict) and isinstance(dict2, dict)
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict):
            merged[key] = merge_dicts(merged[key], value)
        else:
            merged[key] = value
    return merged
