FROM rapidsai/miniforge-cuda:cuda11.8.0-base-ubuntu22.04-py3.9

RUN apt-get update && \
    apt-get install -y libtiff5 git

COPY conda-env.yml /tmp/

RUN mamba env update -n base -f /tmp/conda-env.yml

COPY scripts/python /opt/scripts/basic

WORKDIR /opt

# Installing from source, because this PR is not in the latest release yet (v0.6.2)
# https://github.com/peng-lab/BaSiCPy/commit/d2f4b9fe03efdd6e1bc413d1f9f4340e5d3c2c6a
RUN cd /opt && \
    git clone https://github.com/peng-lab/BaSiCPy.git && \
    cd BaSiCPy && \
    git checkout dev && \
    pip install .

# Downgrade to 0.4.23
RUN pip install --upgrade jax==0.4.23 "jax[cuda11_pip]==0.4.23" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html

COPY Dockerfile /docker

RUN chmod -R 755 /docker