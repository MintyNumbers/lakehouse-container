from deltalake import DeltaTable, write_deltalake
from duckdb import read_csv
from minio import Minio
from pandas import DataFrame


def populate_minio_storage(
    minio_client: Minio,
    storage_options: dict[str, str],
    bucket_name: str,
    table_name: str,
    csv_filepath: str,
):
    table_uri = f"s3a://{bucket_name}/{table_name}"

    # Create new bucket
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

    # Read CSV file with data and write to deltalake
    data: DataFrame = read_csv(csv_filepath).df()
    write_deltalake(
        table_or_uri=table_uri,
        data=data,
        storage_options=storage_options,
    )

    # Print data from deltalake
    dt = DeltaTable(table_uri, storage_options=storage_options)
    print(dt.to_pandas())
