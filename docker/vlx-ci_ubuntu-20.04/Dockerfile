FROM ubuntu:20.04

# add a timestamp for the build. Also, bust the cache.
ADD http://worldclockapi.com/api/json/utc/now /opt/docker/etc/timestamp

RUN apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       apt-transport-https \
       ca-certificates \
       gnupg \
       software-properties-common \
       wget \
    && wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list \
    && apt remove --purge --yes -qq \
       apt-transport-https \
       ca-certificates \
       gnupg \
       software-properties-common \
       wget \
    && apt upgrade --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       build-essential \
       cmake \
       git \
       googletest \
       libgtest-dev \
       libpython3-dev \
       python-is-python3 \
       python3 \
       python3-pip \
       python3-venv \
       python3-requests \
       rsync \
    && apt clean --yes -qq \
    && rm -rf /var/lib/apt/lists/*
