FROM python:3.10-slim

# Install dlib system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    wget \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy your project files
COPY . /app

# Install Python dependencies
# Remove the Windows wheel line if you had it
RUN pip install --upgrade pip
# Add to Dockerfile
ADD https://github.com/z-mahmud22/Dlib_Windows_Python3.x/blob/main/dlib-19.22.99-cp310-cp310-win_amd64.whl /app/dlib.whl
RUN pip install --no-cache-dir /app/dlib.whl


RUN pip install --no-cache-dir -r requirements.txt

# Run your Django server (adjust if using Gunicorn etc.)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
