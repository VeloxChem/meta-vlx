FROM ubuntu:24.04

LABEL org.opencontainers.image.description "GNU-based VeloxChem CI container"

# add a timestamp for the build. Also, bust the cache.
ADD https://timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm /opt/docker/etc/timestamp

# install software
RUN apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       ca-certificates \
       curl \
       bzip2 \
    && curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba \
    && apt purge --yes -qq bzip2 \
    && apt upgrade --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       build-essential \
       cmake \
       g++ \
       gcc \
       git \
       googletest \
       libgtest-dev \
       libhdf5-dev \
       liblapacke \
       liblapacke-dev \
       libopenblas-openmp-dev \
       libpython3-dev \
       mpich \
       ninja-build \
       pkg-config \
       python-is-python3 \
       python3 \
       python3-pip \
       python3-requests \
       python3-venv \
       rsync \
    && curl -Ls https://gitlab.com/libxc/libxc/-/archive/7.0.0/libxc-7.0.0.tar.gz | tar xz \
    && cd libxc-7.0.0 \
    && cmake -S. -Bbuild -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=gcc -DBUILD_SHARED_LIBS=ON -DDISABLE_KXC=OFF -DDISABLE_LXC=OFF -DBUILD_TESTING=OFF > /dev/null 2>&1 \
    && cmake --build build --target install > /dev/null 2>&1 \
    && cd .. \
    && rm -rf libxc-7.0.0 \
    && apt autoremove --yes -qq \
    && apt clean --yes -qq \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && micromamba shell init --shell=bash --root-prefix=~/micromamba

COPY gnu-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/gnu-env.sh" ]

CMD [ "/bin/bash" ]
