from json import dumps, load

from requests import post


def _read_json_params_file(file: str) -> str:
    with open(file) as f:
        json_string = dumps(load(f))
    return json_string


def create_superset_dataset(
    headers: dict[str, str],
    superset_api_url: str,
    table_name: str,
):
    """Create Superset dataset from specified DuckDB table."""

    request_body = {
        "always_filter_main_dttm": "false",
        "database": 1,
        "is_managed_externally": "false",
        "normalize_columns": "false",
        "owners": [1],
        "schema": "duck.main",
        "table_name": table_name,
    }

    response = post(url=f"{superset_api_url}/api/v1/dataset/", headers=headers, json=request_body)
    if response.status_code == 201:
        print("Dataset created successfully")
    else:
        print(f"Failed to create dataset: {response.text}")


def create_superset_chart(
    headers: dict[str, str],
    superset_api_url: str,
    params_file: str,
    table_name: str,
    chart_name: str,
):
    """Create Superset chart from specified Superset dataset."""

    request_body = {
        "dashboards": [],
        "datasource_id": 1,
        "datasource_name": f"duck.main.{table_name}",
        "datasource_type": "table",
        "is_managed_externally": "true",
        "owners": [1],
        "params": _read_json_params_file(params_file),
        "query_context_generation": "true",
        "slice_name": chart_name,
        "viz_type": "echarts_timeseries_bar",
    }

    response = post(url=f"{superset_api_url}/api/v1/chart", headers=headers, json=request_body)
    if response.status_code == 201:
        print("Chart created successfully.")
    else:
        print(f"Failed to create chart: {response.text}")
