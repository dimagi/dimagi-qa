import random
from collections import defaultdict
from functools import cached_property
from typing import Any, Self

import pydantic


class Query(pydantic.BaseModel):
    name: str
    case_types: list[str]
    query_params: dict[str, list[str]]
    value_set_types: list[str] = pydantic.Field(default_factory=list)

    @pydantic.model_validator(mode='before')
    @classmethod
    def ensure_value_set_keys_list(cls, data: Any) -> Any:
        data = cls._value_set_keys_to_list(data)
        return cls._query_params_to_list(data)

    @classmethod
    def _value_set_keys_to_list(cls, data):
        if "value_set_types" not in data:
            data["value_set_types"] = []
        value_set_types = data["value_set_types"]
        data["value_set_types"] = value_set_types if isinstance(value_set_types, list) else [value_set_types]
        return data

    @classmethod
    def _query_params_to_list(cls, data):
        query_params = data["query_params"]
        data["query_params"] = {
            key: value if isinstance(value, list) else [value] for key, value in query_params.items()
        }
        return data

    def get_query_params_for_request(self, value_set=None):
        def _format_value(value):
            if not value_set:
                return value

            return [v.format(**value_set) for v in value]

        return {
            "case_type": self.case_types,
            **{key: _format_value(value) for key, value in self.query_params.items()}
        }


class ValueSet(pydantic.BaseModel):
    type: str
    values: dict[str, str | int | float | bool]


class QueryData(pydantic.BaseModel):
    queries: list[Query]
    value_sets: list[ValueSet]

    @cached_property
    def value_sets_by_key(self):
        by_key = defaultdict(list)
        for value_set in self.value_sets:
            by_key[value_set.type].append(value_set)
        return by_key

    @pydantic.model_validator(mode='after')
    def check_value_sets_exist(self) -> Self:
        for query in self.queries:
            for key in query.value_set_types:
                if key not in self.value_sets_by_key:
                    raise ValueError(f"Value set not found: {key}")
        return self

    def get_random_query(self):
        query = random.choice(self.queries)
        return self._get_query_name_and_data(query)

    def _get_query_name_and_data(self, query):
        merged_values = {}
        for key in query.value_set_types:
            value_set = random.choice(self.value_sets_by_key[key])
            merged_values.update(value_set.values)
        data = query.get_query_params_for_request(merged_values)
        return query.name, data

