FROM rapidsai/miniforge-cuda:cuda11.8.0-base-ubuntu22.04-py3.9

RUN apt-get update && \
    apt-get install -y libtiff5 git

COPY conda-env.yml /tmp/

RUN mamba env update -n base -f /tmp/conda-env.yml

COPY scripts/python /opt/scripts/

WORKDIR /opt

COPY Dockerfile /docker

RUN chmod -R 755 /docker