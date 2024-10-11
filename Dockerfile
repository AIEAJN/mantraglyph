FROM python:3.12.6-slim

# Mettre à jour le système et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    tesseract-ocr \
    wget \
    unzip \
    yasm \
    pkg-config \
    libswscale-dev \
    libtbb-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavformat-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip \
    && pip install poetry
    
ENV PATH="/usr/bin:$PATH"
WORKDIR /app


# copy the project into the docker container
COPY . .
RUN poetry install
# Set permissions to entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Define the entrypoint
ENTRYPOINT ["./entrypoint.sh"]


