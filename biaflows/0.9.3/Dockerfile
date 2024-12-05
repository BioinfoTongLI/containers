FROM python:3.7-slim

# Install git and clean up in the same layer
RUN apt-get update && \
    apt-get install -y git build-essential procps && \
    rm -rf /var/lib/apt/lists/*

COPY ./tests /test_datatest/

RUN pip install https://github.com/Neubias-WG5/biaflows-utilities/archive/refs/tags/v0.9.3.zip \
    fire==0.7.0

# This shouldn't be necessary, to be removed!
RUN git clone https://github.com/cytomine-uliege/Cytomine-python-client.git && \
    cd /Cytomine-python-client && git checkout tags/v2.7.3 && pip install . && \
    rm -r /Cytomine-python-client