FROM joonkeekim/mediar

RUN pip install fire==0.5.0 aicsimageio==4.7.0

# Copy Dockerfile
COPY Dockerfile /docker

# Change permissions
RUN chmod -R 755 /docker