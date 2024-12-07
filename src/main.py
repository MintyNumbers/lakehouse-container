from generate_data import populate_minio_storage
from init_connections import create_duckdb_connection, create_minio_client, create_minio_delta_storage_options


def main():
    duckdb_con = create_duckdb_connection()
    minio_client = create_minio_client()
    storage_options = create_minio_delta_storage_options()

    populate_minio_storage(
        minio_client=minio_client,
        storage_options=storage_options,
        bucket_name="data-bucket",
        table_name="delta-table-2",
        csv_filepath="data/bla.csv",
    )

    duckdb_con.close()


if __name__ == "__main__":
    main()
