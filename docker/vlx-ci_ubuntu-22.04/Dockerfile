FROM ubuntu:22.04

LABEL org.opencontainers.image.description "Base image for VeloxChem CI containers"

# add a timestamp for the build. Also, bust the cache.
ADD https://timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm /opt/docker/etc/timestamp

RUN apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg \
       software-properties-common \
       wget \
       bzip2 \
    && wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list \
    && wget -qO- https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba \
    && apt remove --purge --yes -qq \
       apt-transport-https \
       gnupg \
       software-properties-common \
       wget \
       bzip2 \
    && apt upgrade --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       build-essential \
       cmake \
       git \
       googletest \
       libgtest-dev \
       libhdf5-dev \
       libpython3-dev \
       ninja-build \
       pkg-config \
       python-is-python3 \
       python3 \
       python3-pip \
       python3-requests \
       python3-venv \
       rsync \
    && apt clean --yes -qq \
    && micromamba shell init --shell=bash --prefix=~/micromamba
