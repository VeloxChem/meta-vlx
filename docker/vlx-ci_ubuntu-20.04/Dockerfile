FROM ubuntu:20.04

# add a timestamp for the build. Also, bust the cache.
ADD http://worldclockapi.com/api/json/utc/now /opt/docker/etc/timestamp

RUN apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg \
       software-properties-common \
       wget \
    && wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list \
    && mkdir -p /opt/cmake \
    && curl -Ls https://github.com/Kitware/CMake/releases/download/v3.23.1/cmake-3.23.1-linux-x86_64.tar.gz | tar -xz -C /opt/cmake --strip-components=1 \
    && apt remove --purge --yes -qq \
       apt-transport-https \
       gnupg \
       software-properties-common \
       wget \
    && apt upgrade --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       build-essential \
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
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*
