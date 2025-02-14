FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV VIRTUAL_ENV=/env
ENV PATH=$VIRTUAL_ENV/bin:$VIRTUAL_ENV:$PATH
ENV NUMBA_CACHE_DIR=/tmp
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
        procps git wget build-essential \
        python3 python-is-python3 python3-dev python3-venv

RUN python -m venv $VIRTUAL_ENV && \
    . $VIRTUAL_ENV/bin/activate && \
    pip install --upgrade pip wheel setuptools && \
    pip install shapely tqdm numpy==1.26.4 pandas fire aicsimageio

ENV STARDIST_VERSION=0.9.1
RUN . $VIRTUAL_ENV/bin/activate && \
    pip install 'tensorflow[and-cuda]==2.11.0' && \
    pip install stardist==$STARDIST_VERSION csbdeep gputools edt

COPY Dockerfile /docker/
RUN chmod -R 755 /docker
