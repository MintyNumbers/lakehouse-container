from duckdb import DuckDBPyConnection, connect
from minio import Minio
from requests import post


def create_duckdb_connection() -> DuckDBPyConnection:
    """Connect to persistent DuckDB instance"""

    duckdb_con: DuckDBPyConnection = connect("duckdb-data/duck.db")  # File location of persistent DuckDB instance
    return duckdb_con


def create_minio_client() -> Minio:
    """Connect to running MinIO container."""

    minio_client = Minio(
        endpoint="localhost:9000",  # URL of running MinIO server
        access_key="accesskey",  # Access key to the server (set in compose.yaml)
        secret_key="secretkey",  # Secret key to the server (set in compose.yaml)
        secure=False,
    )
    return minio_client


def create_deltalake_storage_options() -> dict[str, str]:
    """Storage options for writing delta tables to MinIO."""

    storage_options = {
        "endpoint_url": "http://0.0.0.0:9000",  # URL of running MinIO server
        "aws_access_key_id": "accesskey",  # Access key to the server (set in compose.yaml)
        "aws_secret_access_key": "secretkey",  # Secret key to the server (set in compose.yaml)
        "use_ssl": "false",
        "AWS_REGION": "us-east-1",  # Example region
        "signature_version": "s3v4",
        "AWS_ALLOW_HTTP": "true",
        "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
    }

    return storage_options


def create_superset_api_url() -> str:
    """Returns URL of the Superset API."""

    return "http://127.0.0.1:8088"


def create_superset_session_token(superset_api_url: str) -> str:
    """Login to Superset container to generate access token to use API."""

    request_body = {
        "password": "admin",  # Password (set in compose.yaml)
        "provider": "db",
        "refresh": "true",
        "username": "admin",  # Username (set in compose.yaml)
    }
    login_response = post(url=f"{superset_api_url}/api/v1/security/login", json=request_body)
    if login_response.status_code != 200:
        raise Exception(f"Failed to create Superset session token: {login_response.text}")

    return login_response.json()["access_token"]
