FROM python:3.10-slim

# Reduce layer size and memory usage by minimizing packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    pkg-config \
    libx11-dev \
    libatlas-base-dev \
    libgtk-3-dev \
    libboost-all-dev \
    python3-dev \
    wget \
 && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install numpy early to avoid future conflicts
RUN pip install --no-cache-dir --upgrade pip numpy

# Build and install dlib from source (clean build dirs to reduce image size)
WORKDIR /tmp
RUN wget http://dlib.net/files/dlib-19.9.tar.bz2 && \
    tar xjf dlib-19.9.tar.bz2 && \
    cd dlib-19.9 && mkdir build && cd build && \
    cmake .. && cmake --build . --config Release && \
    cd .. && python3 setup.py install && \
    cd / && rm -rf /tmp/*

# Set working directory and copy app
WORKDIR /app
COPY . .

# Install Python dependencies (no cache to reduce layer size)
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
