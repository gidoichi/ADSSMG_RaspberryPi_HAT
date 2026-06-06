FROM python:3.14.5-slim@sha256:c845af9399020c7e562969a13689e929074a10fd057acd1b1fad06a2fb068e97
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt update && apt install -y build-essential && apt clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
