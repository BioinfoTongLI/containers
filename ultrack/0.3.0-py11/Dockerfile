FROM rapidsai/miniforge-cuda:cuda11.8.0-base-ubuntu22.04-py3.9

RUN apt-get update && \
    apt-get install -y git

WORKDIR /opt

# nightly
# RUN pip install git+https://github.com/royerlab/ultrack

# v0.3.0
RUN pip install https://github.com/royerlab/ultrack/archive/refs/tags/v0.3.0.zip
