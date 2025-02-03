FROM kbestak/stardist:0.9.1_cuda12.2

# Set the working directory to /app
WORKDIR /app

ENV NUMBA_CACHE_DIR=/tmp
ENV STARDIST_LOCAL_MODELS_PATH=/models/stardist

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir fire==0.5.0 aicsimageio==4.14.0

# RUN chmod -R 755 /usr/bin/ && chmod -R 755 /opt/

# Copy Dockerfile
COPY Dockerfile /docker

# Change permissions
RUN chmod -R 755 /docker