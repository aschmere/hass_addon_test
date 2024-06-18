FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    sudo \
    git \
    ffmpeg \
    procps \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py /app/app.py
COPY main.py /app/main.py
WORKDIR /app

EXPOSE 5002
# Run the application
CMD ["python", "app.py"]
