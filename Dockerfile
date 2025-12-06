FROM python:3.14.1-slim@sha256:b823ded4377ebb5ff1af5926702df2284e53cecbc6e3549e93a19d8632a1897e
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt update && apt install -y build-essential && apt clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
