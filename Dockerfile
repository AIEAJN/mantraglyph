FROM python:3.11-slim-buster

# Mettre à jour le système et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    yasm \
    pkg-config \
    libswscale-dev \
    libtbb2 \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavformat-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app
# copy the project into the docker container
COPY . .

RUN pip install poetry \
    && poetry install --only main


# Set permissions to scripts.sh
RUN chmod +x ./scp.sh

# Define the entrypoint
ENTRYPOINT ["./scp.sh"]
