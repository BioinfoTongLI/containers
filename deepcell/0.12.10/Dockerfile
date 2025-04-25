FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV VIRTUAL_ENV=/env
ENV PATH=$VIRTUAL_ENV/bin:$VIRTUAL_ENV:$PATH
ENV NUMBA_CACHE_DIR=/tmp
ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/deepcell

RUN apt-get update && apt-get install -y \
        procps git wget build-essential \
        python3 python-is-python3 python3-dev python3-venv

RUN python -m venv $VIRTUAL_ENV && \
    . $VIRTUAL_ENV/bin/activate && \
    pip install --upgrade pip wheel setuptools && \
    pip install imagecodecs ImageTileProcessor==0.1.11

ENV DEEPCELL_VERSION=0.12.10
RUN apt-get update && apt install -y graphviz
RUN . $VIRTUAL_ENV/bin/activate && \
    pip install DeepCell==$DEEPCELL_VERSION

RUN chmod -R 755 /deepcell

COPY Dockerfile /docker/
COPY models /deepcell/.deepcell/models
RUN chmod -R 755 /docker
