from duckdb import DuckDBPyConnection, connect
from minio import Minio
from requests import post


def create_duckdb_connection() -> DuckDBPyConnection:
    """Connect to persistent DuckDB instance"""
    duckdb_con: DuckDBPyConnection = connect("duckdb-data/duck.db")
    return duckdb_con


def create_minio_client() -> Minio:
    """Connect to running MinIO container"""
    minio_client = Minio(
        endpoint="localhost:9000",
        access_key="accesskey",
        secret_key="secretkey",
        secure=False,
    )
    return minio_client


def create_deltalake_storage_options() -> dict[str, str]:
    """Storage options for writing delta tables to MinIO"""

    storage_options = {
        "endpoint_url": "http://0.0.0.0:9000",
        "aws_access_key_id": "accesskey",
        "aws_secret_access_key": "secretkey",
        "use_ssl": "false",
        "AWS_REGION": "us-east-1",
        "signature_version": "s3v4",
        "AWS_ALLOW_HTTP": "true",
        "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
    }

    return storage_options


def create_superset_api_url() -> str:
    return "http://127.0.0.1:8088"


def create_superset_session_token(superset_api_url: str) -> str:
    request_body = {
        "password": "admin",
        "provider": "db",
        "refresh": "true",
        "username": "admin",
    }
    login_response = post(url=f"{superset_api_url}/api/v1/security/login", json=request_body)
    if login_response.status_code != 200:
        raise Exception(f"Failed to create Superset session token: {login_response.text}")

    return login_response.json()["access_token"]
