FROM ghcr.io/veloxchem/meta-vlx/vlx-ci_ubuntu-22.04:sha-56644e9

LABEL org.opencontainers.image.description "GNU-based VeloxChem CI container"

# add a timestamp for the build. Also, bust the cache.
ADD https://timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm /opt/docker/etc/timestamp

# install software
RUN apt install -y gpg-agent wget \
    && wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" |tee /etc/apt/sources.list.d/oneAPI.list \
    && apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -qq \
       -o Dpkg::Options::="--force-confnew" \
       g++ \
       gcc \
       liblapacke \
       liblapacke-dev \
       libopenblas-openmp-dev \
       mpich \
    && curl -Ls https://github.com/grimme-lab/xtb/archive/refs/tags/v6.6.1.tar.gz | tar xz \
    && cd xtb-6.6.1 \
    && cmake -S. -Bbuild -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_Fortran_COMPILER=gfortran -DCMAKE_C_COMPILER=gcc -DBLA_VENDOR=OpenBLAS > /dev/null 2>&1 \
    && rm -rf xtb-6.6.1 \
    && curl -Ls https://github.com/dftd4/dftd4/archive/refs/tags/v3.7.0.tar.gz | tar xz \
    && cd dftd4-3.7.0 \
    && cmake -S. -Bbuild -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_Fortran_COMPILER=gfortran -DCMAKE_C_COMPILER=gcc -DBLA_VENDOR=OpenBLAS -DBUILD_SHARED_LIBS=ON > /dev/null 2>&1 \
    && cmake --build build --target install > /dev/null 2>&1 \
    && cd .. \
    && rm -rf dftd4-3.7.0 \
    && curl -Ls https://gitlab.com/libxc/libxc/-/archive/6.2.2/libxc-6.2.2.tar.gz | tar xz \
    && cd libxc-6.2.2 \
    && cmake -S. -Bbuild -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=gcc -DBUILD_SHARED_LIBS=ON -DDISABLE_KXC=OFF -DDISABLE_LXC=OFF -DBUILD_TESTING=OFF > /dev/null 2>&1 \
    && cmake --build build --target install > /dev/null 2>&1 \
    && cd .. \
    && rm -rf libxc-6.2.2 \
    && apt autoremove --yes -qq \
    && apt clean --yes -qq \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY gnu-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/gnu-env.sh" ]

CMD [ "/bin/bash" ]
