FROM ubuntu:20.04

# add a timestamp for the build. Also, bust the cache.
ADD http://worldclockapi.com/api/json/utc/now /opt/docker/etc/timestamp

# install system packages
RUN apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       apt-transport-https \
       ca-certificates \
       gnupg \
       software-properties-common \
       wget \
    && wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list \
    && apt update --yes -qq \
    && apt upgrade --yes -qq \
    DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
    build-essential \
    cmake \
    g++ \
    gcc \
    git \
    googletest \
    intel-oneapi-compiler-dpcpp-cpp-and-cpp-classic \
    intel-oneapi-mkl \
    intel-oneapi-mkl-devel \
    libgtest-dev \
    libopenblas-openmp-dev \
    libopenblas-dev \
    intel-oneapi-mpi \
    intel-oneapi-mpi-devel \
    intel-oneapi-openmp \
    libopenmpi-dev \
    libpython3-dev \
    openmpi-bin \
    python3 \
    python3-pip \
    python3-venv \
    python-is-python3 \
    rsync \
    && apt remove --yes -qq \
       apt-transport-https \
       ca-certificates \
       gnupg \
       software-properties-common \
       wget \
    && apt autoremove --purge --yes -qq \
    && apt clean --yes -qq \
    && rm -rf /var/lib/apt/lists/*

# copy scripts
COPY intel-env.sh gnu-mkl-env.sh gnu-env.sh /opt/docker/etc

CMD [ "/bin/bash" ]
