# Use the official Python image as a base image
FROM python:3.10-slim

# Install system dependencies required by dlib
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

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "Django_Final.wsgi:application"]
