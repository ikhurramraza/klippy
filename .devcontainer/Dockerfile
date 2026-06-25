# Pin the interpreter from the official image so it always matches .python-version,
# rather than trusting a feature to install a (still very new) 3.14.
FROM python:3.14-slim-bookworm

# Minimal extras the slim image lacks. redis-tools gives `redis-cli` for poking
# at the sidecar; libsecret-tools lets cship read Claude API usage limits; the
# rest are baseline dev/feature prerequisites.
# User creation, zsh, and the GitHub CLI are handled by devcontainer features.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        ca-certificates \
        curl \
        git \
        less \
        libsecret-tools \
        redis-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
