ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:3.19
FROM ${BUILD_FROM}

ENV LANG C.UTF-8

WORKDIR /usr/src/app

# Install Python, bash, and basic tooling
RUN apk add --no-cache python3 py3-pip bash jq && \
    python3 -m ensurepip && \
    pip3 install --no-cache-dir --upgrade pip

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /usr/src/app/homeassistant-addon/run.sh

CMD ["/usr/src/app/homeassistant-addon/run.sh"]
