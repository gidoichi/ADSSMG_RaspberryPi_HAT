FROM python:3.14.4-slim@sha256:2ca02f32b4d9d893863367ce07ec1972819f476dd38d8612f2a9cb6a41cbb727
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt update && apt install -y build-essential && apt clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
