# Case Search Locust Scripts

This load test script performs continuous case search request per user with a constant wait time of 1s between requests.

The query data for each request is selected by randomizing the data in the query YAML configuration file.

Run from `LocustScripts` directory:

```shell
locust -f case_search/locustfile.py --headless -u 1 -r 1 \
  --host http://localhost:8000 \
  --domain skelly-1 \
  --app-id b62974969e57051ad70160a798ed79e8  \
  --queries case_search/co_carecoordination_queries.yml \
  --user-details case_search/user_credentials_example.json
```

## Options

- `--host` - URL of the application
- `--domain` - Domain of the application
- `--app-id` - Application ID
- `--queries` - Path to the queries file
- `--user-details` - Path to the user credentials file

## Request generation

Each request is generated as follows:

1. Select a random query from the list of queries provided.
2. Select random value sets for the query using the `query.value_set_types` field.
3. Fill in the query parameters with values from the value set.
4. Send the request.

## Queries file

This YAML file contains request data that will be used by the locust scripts to perform case search requests.

### Queries ("queries" key)
A list of parameterized queries. Each request will select one query at random and fill in the
parameters with values from a random value set.

Query fields:
- `name`: The name of the query (used for logging)
- `case_types`: A list of case types to pass via the 'case_type' query parameter (required)
- `value_set_types`: (optional) The value set types to use to select a value set data for the query at runtime. If
  multiple types are provided, the data will be merged into a single dictionary before filling in the query parameters.
- `query_params`: A dictionary of query parameters to pass in the request. They query values may contain
  variable references using the '{name}' syntax which will be filled by values from the value set. The values
  of the dictionary may be a string or a list.

```yaml
queries:
  - name: test
    case_types: [client]
    value_set_types: client
    query_params:
      case_name: {case_name}
      _xpath_query:
        - first_name='{first_name}' and last_name='{last_name}'
        - subcase-exists('parent', @case_type = 'alias' and first_name='{first_name}' and last_name='{last_name}')
```

### Value Sets ("value_sets" key)
A list of parameter values which are used to format the queries.

Value set fields:
- `type`: A string which indicates which type of value set this is. A value set with
  a type matching `query.value_set_types` will be selected at runtime.
- `values`: A dictionary of values which are used to format the query at runtime. The keys in this dictionary are used
  to replace the variable references in the query parameters.

```yaml
value_sets:
  - type: client
    values:
      first_name: bob
      last_name: smith
      alias: bobby
```
