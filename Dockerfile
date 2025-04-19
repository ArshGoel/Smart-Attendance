# Use a Python image as the base image
FROM python:3.9-slim

# Install system dependencies for building dlib
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

# Copy the project files to the container's /app directory
COPY . /app

# If you have a pre-built dlib wheel in the static folder, copy it to the container
# Assuming the wheel file is located in the static folder at /static/dlib.whl
COPY static/Dlib/dlib-19.22.99-cp310-cp310-win_amd64.whl /app/dlib-19.22.99-cp310-cp310-win_amd64.whl

# Install the required Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install dlib from the pre-built wheel file (if available)
RUN pip install --no-cache-dir /app/dlib-19.22.99-cp310-cp310-win_amd64.whl

# Expose the port that the Django app will run on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "Django_Final.wsgi:application"]
