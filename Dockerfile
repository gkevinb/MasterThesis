# Use an official Python 3.6 image
FROM python:3.6-slim

# Set environment variables to avoid buffer issues
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install system dependencies for tkinter and others
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    tk-dev \
    tcl-dev \
    libffi-dev \
    libssl-dev \
    libbz2-dev \
    zlib1g-dev \
    libsqlite3-dev \
    libreadline-dev \
    libtk8.6 libx11-6 libx11-dev \
    python3-tk \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip==19.2.3 \
    && pip install -r requirements.txt

# Copy the rest of your application code to /app
COPY . .

# Specify the command to run the app (update as needed)
CMD ["python", "analysisFT.py"]
