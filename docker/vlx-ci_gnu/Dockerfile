FROM ghcr.io/veloxchem/meta-vlx/vlx-ci_ubuntu-22.04:sha-56644e9

LABEL org.opencontainers.image.description "GNU-based VeloxChem CI container"

# add a timestamp for the build. Also, bust the cache.
ADD https://timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm /opt/docker/etc/timestamp

# install software
RUN apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -qq \
       -o Dpkg::Options::="--force-confnew" \
       g++ \
       gcc \
       liblapacke \
       liblapacke-dev \
       libopenblas-openmp-dev \
       libopenmpi-dev \
       openmpi-bin \
    && curl -Ls https://github.com/grimme-lab/xtb/archive/refs/tags/v6.6.0.tar.gz | tar xz \
    && cd xtb-6.6.0 \
    && cmake -S. -Bbuild -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_Fortran_COMPILER=gfortran -DCMAKE_C_COMPILER=gcc -DBLA_VENDOR=OpenBLAS > /dev/null 2>&1 \
    && cmake --build build --target install > /dev/null 2>&1 \
    && cd .. \
    && rm -rf xtb-6.6.0 \
    && curl -Ls https://gitlab.com/libxc/libxc/-/archive/6.1.0/libxc-6.1.0.tar.gz | tar xz \
    && cd libxc-6.1.0 \
    && cmake -S. -Bbuild -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=gcc -DBUILD_SHARED_LIBS=ON -DBUILD_TESTING=OFF > /dev/null 2>&1 \
    && cmake --build build --target install > /dev/null 2>&1 \
    && cd .. \
    && rm -rf libxc-6.1.0 \
    && apt autoremove --yes -qq \
    && apt clean --yes -qq \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY gnu-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/gnu-env.sh" ]

CMD [ "/bin/bash" ]
