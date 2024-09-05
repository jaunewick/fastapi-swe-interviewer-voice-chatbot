# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION} as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required for building packages like h5py
RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    python3 -m pip install --upgrade pip

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry and pip for specific packages
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

CMD poetry run fastapi dev app/main.py --host 0.0.0.0 --reload