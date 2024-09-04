# Use multi-stage builds
FROM rapidsai/miniforge-cuda:cuda11.8.0-base-ubuntu22.04-py3.11 as builder

# Install git and clean up in the same layer
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt

# Copy only the necessary files
COPY conda-env.yml /tmp/
COPY scripts/python /scripts/
COPY Dockerfile /docker

# Update environment and set permissions in the same layer
RUN mamba env update -n base -f /tmp/conda-env.yml && \
    chmod -R 755 /usr/bin/ && \
    chmod -R 755 /scripts/ && \
    chmod -R 755 /docker && \
    chmod -R 755 /opt/conda/bin/

# Final stage
FROM rapidsai/miniforge-cuda:cuda11.8.0-base-ubuntu22.04-py3.11

COPY --from=builder /opt /opt
COPY --from=builder /scripts /scripts
COPY --from=builder /docker /docker

WORKDIR /opt