from duckdb import DuckDBPyConnection, connect
from minio import Minio


def create_duckdb_connection() -> DuckDBPyConnection:
    """Connect to persistent DuckDB instance"""
    duckdb_con: DuckDBPyConnection = connect("duckdb-data/duck.db")
    return duckdb_con


def create_minio_client() -> Minio:
    """Connect to running MinIO container"""
    minio_client = Minio(
        endpoint="localhost:9000",  # Replace with your MinIO server address
        access_key="accesskey",
        secret_key="secretkey",
        secure=False,  # Set to True if using HTTPS
    )
    return minio_client


def create_minio_delta_storage_options() -> dict[str, str]:
    """Storage options for writing delta tables to MinIO"""

    storage_options = {
        "endpoint_url": "http://0.0.0.0:9000",
        "aws_access_key_id": "accesskey",
        "aws_secret_access_key": "secretkey",
        "use_ssl": "false",
        "AWS_REGION": "us-east-1",  # Example region
        "signature_version": "s3v4",
        "AWS_ALLOW_HTTP": "true",
        "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
    }

    return storage_options
