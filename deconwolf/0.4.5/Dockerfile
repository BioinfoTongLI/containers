FROM ubuntu:22.04

ENV TZ=Etc/UTC

# Install tzdata noninteractively first, then the rest; also drop sudo in Docker
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && \
    apt-get install -y --no-install-recommends unzip wget cmake build-essential \
    pkg-config gcc libfftw3-single3 libfftw3-dev libgsl-dev libomp-dev libpng-dev libtiff-dev && rm -rf /var/lib/apt/lists/*

RUN wget --no-check-certificate https://github.com/elgw/deconwolf/archive/refs/tags/v0.4.5.zip && \
    unzip v0.4.5.zip && rm -rf /var/lib/apt/lists/*

RUN cd deconwolf-0.4.5 && mkdir builddir && \
    cd builddir && cmake .. && cmake --build . &&  make install