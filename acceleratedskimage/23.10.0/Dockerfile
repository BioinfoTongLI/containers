FROM rapidsai/miniforge-cuda:cuda11.8.0-base-ubuntu22.04-py3.11

RUN apt-get update && \
    apt-get install -y git

WORKDIR /opt

# RUN mamba install pytorch torchvision pytorch-cuda=11.8 -c pytorch -c nvidia -y && pip install spotiflow
COPY conda-env.yml /tmp/

RUN mamba env update -n base -f /tmp/conda-env.yml


COPY scripts/python /opt/scripts/
