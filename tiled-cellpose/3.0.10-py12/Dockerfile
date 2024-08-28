# FROM quay.io/biocontainers/cellpose:3.0.8
FROM rapidsai/miniforge-cuda:cuda12.5.1-base-ubuntu22.04-py3.12

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY scripts/python /scripts/

COPY Dockerfile /docker

RUN chmod -R 755 /docker