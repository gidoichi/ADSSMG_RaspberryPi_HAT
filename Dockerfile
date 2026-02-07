FROM python:3.14.3-slim@sha256:486b8092bfb12997e10d4920897213a06563449c951c5506c2a2cfaf591c599f
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt update && apt install -y build-essential && apt clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
