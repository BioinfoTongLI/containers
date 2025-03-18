FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV VENV_PATH=/env
ENV PATH=$VENV_PATH/bin:$PATH
ENV NUMBA_CACHE_DIR=/tmp

RUN apt-get update && apt-get install -y \
        procps git wget build-essential unzip \
        python3 python-is-python3 python3-dev python3-venv

RUN python -m venv $VENV_PATH && \
    . $VENV_PATH/bin/activate && \
    pip install --upgrade pip wheel setuptools && \
    pip install imagecodecs opencv-python-headless ImageTileProcessor==0.1.9

# install package
RUN apt-get update && apt-get install -y default-jre zlib1g-dev
RUN git clone https://github.com/instanseg/instanseg.git /opt/instanseg && \
    . $VENV_PATH/bin/activate && \
    pip install 'torch==2.4.1+cu121' --index-url https://download.pytorch.org/whl/cu121 && \
    pip install slideio 'bfio[all]' && \
    pip install /opt/instanseg

# download models
RUN mkdir -p /opt/instanseg/models && \
    cd /tmp && \
    wget https://github.com/instanseg/instanseg/releases/download/instanseg_models_v1/brightfield_nuclei.zip && \
    wget https://github.com/instanseg/instanseg/releases/download/instanseg_models_v1/fluorescence_nuclei_and_cells.zip && \
    unzip /tmp/brightfield_nuclei.zip -d /opt/instanseg/models && rm /tmp/brightfield_nuclei.zip && \
    unzip /tmp/fluorescence_nuclei_and_cells.zip -d /opt/instanseg/models && rm /tmp/fluorescence_nuclei_and_cells.zip

COPY Dockerfile /docker/
RUN chmod -R 755 /docker
