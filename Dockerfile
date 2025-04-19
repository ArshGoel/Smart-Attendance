FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    cmake \
    pkg-config \
    libx11-dev \
    libatlas-base-dev \
    libgtk-3-dev \
    libboost-all-dev \
    python3-dev \
    python3-pip \
 && apt-get clean

# Install numpy
RUN pip3 install --upgrade pip numpy

# Build and install dlib from source
WORKDIR /tmp
RUN wget http://dlib.net/files/dlib-19.9.tar.bz2 && \
    tar xvf dlib-19.9.tar.bz2 && \
    cd dlib-19.9 && \
    mkdir build && cd build && \
    cmake .. && cmake --build . --config Release && \
    cd .. && python3 setup.py install && \
    cd / && rm -rf /tmp/*

# Set working directory
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir dlib

# Start your app (adjust this line)
CMD ["gunicorn", "yourproject.wsgi:application", "--bind", "0.0.0.0:8000"]