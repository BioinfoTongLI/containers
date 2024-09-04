# Use an official Python runtime as a parent image
FROM rapidsai/miniforge-cuda:cuda12.5.1-base-ubuntu22.04-py3.12

# Set the working directory to /app
WORKDIR /app

# Copy only the necessary files
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Remove requirements.txt after installing Python dependencies
RUN rm requirements.txt

# Copy the current directory contents into the container at /app
COPY scripts/python /scripts/

# Copy Dockerfile
COPY Dockerfile /docker

# Change permissions
RUN chmod -R 755 /docker && chmod -R 755 /usr/bin/