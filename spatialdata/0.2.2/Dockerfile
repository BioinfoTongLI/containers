FROM rapidsai/miniforge-cuda:cuda11.8.0-base-ubuntu22.04-py3.11

RUN apt-get update && \
    apt-get install -y git

COPY conda-env.yml /tmp/

RUN mamba env update -n base -f /tmp/conda-env.yml

COPY scripts/python /scripts/

COPY Dockerfile /docker

RUN chmod -R 755 /docker && \
    chmod -R 755 /opt