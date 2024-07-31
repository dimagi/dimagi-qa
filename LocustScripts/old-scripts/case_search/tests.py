import pathlib
from unittest import mock

import pytest

from case_search.loader import load_query_data
from case_search.models import Query, QueryData, ValueSet


@pytest.mark.parametrize("query_data", [
    pytest.param(
        {"name": "query1", "case_types": ["case1"], "query_params": {"param1": ["value1"]}, "value_set_types": "type1"},
        id="value_set_types to list",
    ),
    pytest.param(
        {"name": "query1", "case_types": ["case1"], "query_params": {"param1": "value1"}, "value_set_types": ["type1"]},
        id="param values to list",
    ),
])
def test_query_model_values_to_list(query_data):
    query = Query(**query_data)
    assert query == Query(
        name="query1",
        case_types=["case1"],
        query_params={"param1": ["value1"]},
        value_set_types=["type1"],
    )


def test_query_model_values_none():
    query = Query(name="query1", case_types=["case1"], query_params={})
    assert query == Query(
        name="query1",
        case_types=["case1"],
        query_params={},
        value_set_types=[],
    )


def test_get_query_params_for_request():
    query = Query(name="query1", case_types=["case1"], query_params={
        "param1": ["{value1}"],
        "param2": ["{value1}={value2}", "{value2}"],
    })

    assert query.get_query_params_for_request({"value1": "value1", "value2": "value2"}) == {
        "case_type": ["case1"],
        "param1": ["value1"],
        "param2": ["value1=value2", "value2"],
    }


@pytest.mark.parametrize(("query", "value_sets", "expected_data"), [
    pytest.param(
        Query(name="query1", case_types=["case1"], query_params={"param1": ["value1"]}),
        [],
        {"case_type": ["case1"], "param1": ["value1"]},
        id="no_value_set",
    ),
    pytest.param(
        Query(name="query1", case_types=["case1"], query_params={"param1": ["{value_key1}"]}, value_set_types=["type1"]),
        [ValueSet(type="type1", values={"value_key1": "value1"})],
        {"case_type": ["case1"], "param1": ["value1"]},
        id="single_value_set",
    ),
    pytest.param(
        Query(
            name="query3",
            case_types=["case2"],
            query_params={"param2": ["{value_key1}", "{value_key2}"]},
            value_set_types=["type1", "type2"],
        ),
        [
            ValueSet(type="type1", values={"value_key1": "value1"}),
            ValueSet(type="type2", values={"value_key2": "value2"}),
        ],
        {"case_type": ["case2"], "param2": ["value1", "value2"]},
        id="multiple_value_sets",
    ),
])
def test_get_query_name_and_data(query, value_sets, expected_data):
    data = QueryData(queries=[query], value_sets=value_sets)
    name, request_data = data._get_query_name_and_data(query)
    assert request_data == expected_data


@mock.patch("case_search.loader._get_reference_path")
@mock.patch("case_search.loader.load_yaml_data")
@mock.patch("case_search.loader.load_csv_data")
def test_load_query_data(load_csv_data, load_yaml_data, _):
    load_yaml_data.return_value = {
        "queries": [
            {"name": "query1", "case_types": ["case1"], "query_params": {"param1": ["value1"]}},
        ],
        "value_sets": [
            {"type": "type1", "values": {"value_key1": "value1"}},
            {"path": "value_sets.csv", "type": "type2", "format": "csv"},
        ],
    }
    load_csv_data.return_value = [
        {"a": "a1", "b": "b1"},
        {"a": "a2", "b": "b2"},
    ]
    query_data = load_query_data(pathlib.Path("co_carecoordination_queries.yml"))
    assert query_data == QueryData(
        queries=[
            Query(name="query1", case_types=["case1"], query_params={"param1": ["value1"]}),
        ],
        value_sets=[
            ValueSet(type="type1", values={"value_key1": "value1"}),
            ValueSet(type="type2", values={"a": "a1", "b": "b1"}),
            ValueSet(type="type2", values={"a": "a2", "b": "b2"}),
        ],
    )
