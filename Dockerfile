FROM python:3.10-slim

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     cmake \
#     pkg-config \
#     libx11-dev \
#     libatlas-base-dev \
#     libgtk-3-dev \
#     libboost-all-dev \
#     python3-dev \
#     wget \
#     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# RUN pip install --no-cache-dir numpy

# Build dlib from source
WORKDIR /tmp
RUN wget http://dlib.net/files/dlib-19.9.tar.bz2 && \
    tar xvf dlib-19.9.tar.bz2 && \
    cd dlib-19.9 && \
    mkdir build && cd build && \
    cmake .. && cmake --build . --config Release && \
    cd .. && python3 setup.py install && \
    cd / && rm -rf /tmp/*
