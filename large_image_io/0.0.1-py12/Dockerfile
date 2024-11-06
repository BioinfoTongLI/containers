FROM python:3.12-slim

# RUN apt-get update && \
#     apt-get install -y libtiff5 git

COPY scripts/python /opt/scripts/
COPY requirements.txt /opt/scripts/

RUN pip install --no-cache-dir -r /opt/scripts/requirements.txt

WORKDIR /opt

COPY Dockerfile /docker

RUN chmod -R 755 /docker