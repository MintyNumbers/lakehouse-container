from generate_data import create_duckdb_table_from_minio, populate_minio_storage
from init_connections import (
    create_deltalake_storage_options,
    create_duckdb_connection,
    create_minio_client,
    create_superset_api_url,
    create_superset_session_token,
)
from superset_visualization import create_superset_chart, create_superset_dataset


def main():
    # Populate MinIO object storage with Deltalake tables containing the downloaded data
    storage_options = create_deltalake_storage_options()
    minio_client = create_minio_client()
    populate_minio_storage(
        minio_client=minio_client,
        storage_options=storage_options,
        bucket_name="data-bucket",
        table_name="delta-table-3",
        csv_filepath="data/shopping_trends.csv",
    )

    # Create DuckDB table with some data from MinIO
    duckdb_con = create_duckdb_connection()
    create_duckdb_table_from_minio(
        minio_bucket_name="delta-bucket",
        storage_options=storage_options,
        con=duckdb_con,
        delta_table_name="delta-table-3",
        duckdb_table_name="my_table",
    )
    duckdb_con.close()

    # Create dataset and charts using data from DuckDB
    superset_api_url = create_superset_api_url()
    superset_session_token = create_superset_session_token(superset_api_url)
    HEADERS = {"Authorization": f"Bearer {superset_session_token}", "Content-Type": "application/json"}
    create_superset_dataset(
        headers=HEADERS,
        superset_api_url=superset_api_url,
        table_name="my_table",  # has to be the same as duckdb_table_name="my_table"
    )
    create_superset_chart(
        headers=HEADERS,
        superset_api_url=superset_api_url,
        params_file="superset-params/create-chart.json",
        table_name="my_table",  # has to be the same as table_name="my_table"
        chart_name="my_chart",
    )


if __name__ == "__main__":
    main()
