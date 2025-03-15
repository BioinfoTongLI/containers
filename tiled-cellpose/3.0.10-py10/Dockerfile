# Use an official Python runtime as a parent image
FROM rapidsai/miniforge-cuda:cuda12.5.1-base-ubuntu22.04-py3.10

# Set the working directory to /app
WORKDIR /app

ENV NUMBA_CACHE_DIR=/tmp
ENV CELLPOSE_LOCAL_MODELS_PATH=/models/cellpose

# Copy only the necessary files
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R 755 /usr/bin/ && chmod -R 755 /opt/

# Copy the current directory contents into the container at /app
COPY scripts/python /scripts/

RUN python -c "from cellpose import core, io, models; model = models.Cellpose(model_type='cyto3')"

RUN chmod -R 755 $CELLPOSE_LOCAL_MODELS_PATH

# Copy Dockerfile
COPY Dockerfile /docker

# Change permissions
RUN chmod -R 755 /docker