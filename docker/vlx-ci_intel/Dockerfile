FROM ghcr.io/enccs/meta-vlx/vlx-ci_ubuntu-22.04:sha-2d80890

LABEL org.opencontainers.image.description "Intel-based container for VeloxChem CI"

# add a timestamp for the build. Also, bust the cache.
ADD https://timeapi.io/api/Time/current/zone?timeZone=Europe/Stockholm /opt/docker/etc/timestamp

# install software
RUN apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -qq \
       -o Dpkg::Options::="--force-confnew" \
       intel-oneapi-compiler-dpcpp-cpp-and-cpp-classic \
       intel-oneapi-compiler-fortran \
       intel-oneapi-mkl \
       intel-oneapi-mkl-devel \
       intel-oneapi-mpi \
       intel-oneapi-mpi-devel \
       intel-oneapi-openmp \
    && curl -Ls https://github.com/grimme-lab/xtb/archive/refs/tags/v6.5.0.tar.gz | tar xz \
    && cd xtb-6.5.0 \
    && . /opt/intel/oneapi/setvars.sh \
    && cmake -S. -Bbuild -GNinja -DCMAKE_Fortran_COMPILER=ifort -DCMAKE_C_COMPILER=icc -DCMAKE_BUILD_TYPE=Release > /dev/null 2>&1 \
    && cmake --build build --target install > /dev/null 2>&1 \
    && cd .. \
    && rm -rf xtb-6.5.0 \
    && curl -Ls https://gitlab.com/libxc/libxc/-/archive/6.0.0/libxc-6.0.0.tar.gz | tar xz \
    && cd libxc-6.0.0 \
    && cmake -S. -Bbuild -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=icc -DBUILD_SHARED_LIBS=ON -DENABLE_XHOST=ON -DDISABLE_KXC=OFF -DDISABLE_LXC=OFF -DBUILD_TESTING=OFF > /dev/null 2>&1 \
    && cmake --build build --target install > /dev/null 2>&1 \
    && cd .. \
    && rm -rf libxc-6.0.0 \
    && apt autoremove --yes -qq \
    && apt clean --yes -qq \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY intel-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/intel-env.sh" ]

CMD [ "/bin/bash" ]
