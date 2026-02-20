FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    rustc cargo \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /Snippets


# Copy Python dependency file
COPY requirements.txt /tmp/requirements.txt

# Install Python packages
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

CMD ["sleep", "infinity"]