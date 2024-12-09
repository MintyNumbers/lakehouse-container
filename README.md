# Lakehouse Container with FOSS (MinIO, Deltalake, DuckDB and Superset)
Example implementation of a lakehouse container.

## Description
Project with MinIO and Superset containers in the same network. Superset is connected to a DuckDB instance to query parquet files in MinIO Deltalake tables (Lakehouse architecture).



## Get Started

### Dependencies

To execute this example you will need:

Python 3 with libraries listed in `requirements.txt`. You can create a virtual environment in the .venv
project directory:

```bash
# Linux, Unix
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip --version
# OR: Windows
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip --version
```

Then you can install the libraries:

```bash
# Linux, Unix
python3 -m pip install -r requirements.txt
# OR: Windows
py -m pip install -r requirements.txt
```

Alternatively you can also use Anaconda:

```bash
conda create -n example minio==7.1.0 python-duckdb==1.1.3 conda-forge::deltalake==0.18.2 pandas==2.0.3 requests==2.32.3 python==3.11.10
conda activate example
```

You will also need Docker or Podman-Compose to execute `docker-compose.yml`.


### Installation
The program's code is found at: https://github.com/MintyNumbers/lakehouse-container.
You can download the repository using `git clone`:

```bash
git clone git@github.com:MintyNumbers/lakehouse-container.git
```


### Executing program

#### Dataset
First you need to download the Customer Shopping dataset that we want to store and visualize from Kaggle:

https://www.kaggle.com/datasets/bhadramohit/customer-shopping-latest-trends-dataset

Download and unzip this file to the `data` directory in the project folder.

#### MinIO and Superset containers

Then, we build the Apache Superset image:

```bash
# Podman
podman build --format docker -f superset-duckdb.dockerfile -t superset-duckdb .
# OR: Docker
docker build -f superset-duckdb.dockerfile -t superset-duckdb .
```

To execute the program we will need to start the MinIO and Apache Superset containers using `docker compose`:

Note: To execute `compose.yaml` you will require an internet connection to download the required images.

```bash
# Podman
podman-compose up
# OR: Docker
docker compose up
```

#### Populating the storage with the downloaded dataset and visualizing it

Now you can execute the main function to populate the MinIO storage with data that we want to visualize:

```bash
python src/main.py
```

#### View the visualizations
To log into Apache Superset at http://127.0.0.1:8088 you can use the default credentials: admin/admin. Similarly, the MinIO storage can be accessed at http://0.0.0.0:9001/ using accesskey/secretkey.



## Sources

[1] https://docs.docker.com/reference/compose-file/services

[2] https://docs.docker.com/reference/dockerfile/

[3] https://github.com/cnstlungu/portable-data-stack-dagster/blob/main/docker-compose.yml

[4] https://jorritsandbrink.substack.com/p/open-source-data-viz-with-superset

[5] https://github.com/delta-io/delta-rs

[6] https://duckdb.org/docs/guides/python/import_pandas.html

[7] https://superset.apache.org/docs/api/ or interactively (locally): http://127.0.0.1:8088/swagger/v1
