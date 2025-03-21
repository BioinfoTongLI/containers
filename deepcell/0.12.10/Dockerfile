# Base image
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

# Environment variables
ENV VIRTUAL_ENV=/env
ENV PATH=$VIRTUAL_ENV/bin:$VIRTUAL_ENV:$PATH
ENV NUMBA_CACHE_DIR=/tmp
ENV DEBIAN_FRONTEND=noninteractive
ENV DEEPCELL_VERSION=0.12.10

# Redefine home folder
ENV HOME=/deepcell
WORKDIR $HOME

# Ensure the new home directory exists
RUN mkdir -p $HOME

# Install system dependencies
RUN apt-get update && apt-get install -y \
        procps git wget build-essential \
        python3 python-is-python3 python3-dev python3-venv \
        graphviz && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up Python virtual environment and install Python dependencies
RUN python3 -m venv $VIRTUAL_ENV && \
    . $VIRTUAL_ENV/bin/activate && \
    pip install --upgrade pip wheel setuptools && \
    pip install imagecodecs ImageTileProcessor==0.1.11 DeepCell==$DEEPCELL_VERSION

# Copy necessary files
COPY Dockerfile /docker/
COPY models $HOME/.deepcell/models

# Set permissions
RUN chmod -R 755 /docker
