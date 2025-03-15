FROM rapidsai/miniforge-cuda:cuda11.8.0-base-ubuntu22.04-py3.10

RUN apt-get update && \
    apt-get install -y git

COPY requirements.txt /tmp/requirements.txt

RUN pip install -U -r /tmp/requirements.txt --no-cache-dir

COPY Dockerfile /docker

RUN chmod -R 755 /docker && chmod -R 755 /opt