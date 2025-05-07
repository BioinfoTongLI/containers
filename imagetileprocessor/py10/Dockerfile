FROM python:3.10.0-slim

# Set the working directory to /app
# WORKDIR /app

# Set environment variables
ENV NUMBA_CACHE_DIR=\$PWD

# Update and install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps openjdk-17-jre && \ 
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir ImageTileProcessor==0.1.15 pyarrow==19.0.1 bioformats_jar==2020.5.27

# Set permissions
RUN chmod -R 755 /usr/bin/ && chmod -R 755 /opt/

# Copy Dockerfile
COPY Dockerfile /docker

# Change permissions
RUN chmod -R 755 /docker