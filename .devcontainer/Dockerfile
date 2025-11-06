# Bazine aplinka su Ubuntu
FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Įdiegiame Python ir pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Įdiegiame PHP ir Composer
RUN apt-get install -y php-cli composer

# Nustatome numatytą darbo katalogą
WORKDIR /workspaces

# Nustatome numatytą shell
SHELL ["/bin/bash", "-c"]
