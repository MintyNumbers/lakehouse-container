# Lakehouse Container with FOSS
Example implementation of a lakehouse container.

## Description
TODO

## Get Started
TODO

### Dependencies

To execute this example you will need:

Python 3 with libraries listed in `requirements.txt`. You can create a virtual environment in the .venv
project directory:

```bash
# Unix, macOS
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
# Unix, macOS
python3 -m pip install -r requirements.txt
# OR: Windows
py -m pip install -r requirements.txt
```

You will also need Docker or Podman-Compose to execute `docker-compose.yml`.


### Installation
The program's code is found at: https://github.com/MintyNumbers/lakehouse-container.
You can download the repository using `git clone`:

```bash
git clone https://github.com/MintyNumbers/lakehouse-container.git
```

### Executing program

First you will need to build the Apache Superset image:

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

To log into Apache Superset at http://127.0.0.1:8088 you can use the default credentials: admin/admin


TODO


## Sources

[1] https://docs.docker.com/reference/compose-file/services

[2] https://docs.docker.com/reference/dockerfile/

[3] https://github.com/cnstlungu/portable-data-stack-dagster/blob/main/docker-compose.yml

[4] https://jorritsandbrink.substack.com/p/open-source-data-viz-with-superset

[5]
