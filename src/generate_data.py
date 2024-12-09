from deltalake import DeltaTable, write_deltalake
from duckdb import DuckDBPyConnection, read_csv, sql
from minio import Minio
from pandas import DataFrame


def populate_minio_storage(
    minio_client: Minio,
    storage_options: dict[str, str],
    bucket_name: str,
    table_name: str,
    csv_filepath: str,
):
    """Populate the MinIO storage in specified delta table in specified bucket with data using a given CSV file."""

    # Create new bucket
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    # Read CSV file with data and write to deltalake
    table_uri = f"s3a://{bucket_name}/{table_name}"
    data: DataFrame = read_csv(csv_filepath).df()
    write_deltalake(
        table_or_uri=table_uri,
        data=data,
        storage_options=storage_options,
    )

    # Print data from deltalake
    dt = DeltaTable(table_uri, storage_options=storage_options)
    print(dt.to_pandas())


def create_duckdb_table_from_minio(
    minio_bucket_name: str,
    storage_options: dict[str, str],
    con: DuckDBPyConnection,
    delta_table_name: str,
    duckdb_table_name: str,
):
    """Creates table in persistent DuckDB instance using data from specified delta table from specific MinIO bucket."""

    # Query Deltalake table in MinIO bucket
    my_df: DataFrame = DeltaTable(  # noqa: F841
        table_uri=f"s3a://{minio_bucket_name}/{delta_table_name}",
        storage_options=storage_options,
    ).to_pandas()

    # Write queried data to persistent DuckDB storage connected to Superset
    sql(f"CREATE TABLE {duckdb_table_name} AS SELECT * FROM my_df", connection=con)
    sql(f"INSERT INTO {duckdb_table_name} SELECT * FROM my_df", connection=con)
    sql(f"SELECT * FROM {duckdb_table_name}", connection=con).show()
