FROM ubuntu:20.04 AS base

# Add a timestamp for the build. Also, bust the cache.
ADD http://worldclockapi.com/api/json/utc/now /opt/docker/etc/timestamp

# Install system packages
RUN apt-get update --yes -qq
RUN DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
        apt-transport-https \
        ca-certificates \
        gnupg \
        software-properties-common \
        wget
RUN wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null
RUN echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | tee /etc/apt/sources.list.d/oneAPI.list
RUN apt update --yes -qq
RUN apt upgrade --yes -qq
RUN apt remove --yes -qq \
        apt-transport-https \
        ca-certificates \
        gnupg \
        software-properties-common \
        wget
RUN apt autoremove --purge --yes -qq

FROM base AS deps
RUN DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
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
        python-is-python3
RUN apt clean --yes -qq
RUN rm -rf /var/lib/apt/lists/*

FROM deps AS prep-env
# copy scripts
COPY intel-env.sh /opt/docker/etc/intel-env.sh
COPY gnu-mkl-env.sh /opt/docker/etc/gnu-mkl-env.sh
COPY gnu-env.sh /opt/docker/etc/gnu-env.sh

FROM prep-env
CMD [ "/bin/bash" ]
