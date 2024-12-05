FROM apache/superset:4.1.1-dev

USER root

RUN pip install --upgrade pip
RUN pip install duckdb==1.1.3
RUN pip install duckdb-engine==0.13.6

COPY --chown=superset ./superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset