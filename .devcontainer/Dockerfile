FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y openjdk-21-jdk python3 python3-pip git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest antlr4-python3-runtime==4.13.2 pytest-timeout

WORKDIR /workspace

COPY . /workspace

COPY .devcontainer/CS /usr/local/bin/CS
RUN chmod +x /usr/local/bin/CS