FROM rapidsai/miniforge-cuda:cuda11.8.0-base-ubuntu22.04-py3.9

RUN apt-get update && \
    apt-get install -y git

WORKDIR /opt

RUN pip install https://github.com/royerlab/ultrack/archive/refs/tags/v0.5.0.zip

COPY Dockerfile /docker

RUN chmod -R 755 /docker