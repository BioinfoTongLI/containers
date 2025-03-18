FROM python:3.10.0-slim

# Set the working directory to /app
WORKDIR /app

ENV NUMBA_CACHE_DIR=\$PWD

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir ImageTileProcessor==0.1.9 pyarrow==19.0.1

RUN chmod -R 755 /usr/bin/ && chmod -R 755 /opt/

# Copy Dockerfile
COPY Dockerfile /docker

# Change permissions
RUN chmod -R 755 /docker