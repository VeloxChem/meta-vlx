FROM ghcr.io/veloxchem/meta-vlx/vlx-ci_ubuntu-22.04:sha-56644e9

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
    && . /opt/intel/oneapi/setvars.sh \
    && curl -Ls https://gitlab.com/libxc/libxc/-/archive/7.0.0/libxc-7.0.0.tar.gz | tar xz \
    && cd libxc-7.0.0 \
    && cmake -S. -Bbuild -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=icx -DBUILD_SHARED_LIBS=ON -DENABLE_XHOST=ON -DDISABLE_KXC=OFF -DDISABLE_LXC=OFF -DBUILD_TESTING=OFF > /dev/null 2>&1 \
    && cmake --build build --target install > /dev/null 2>&1 \
    && cd .. \
    && rm -rf libxc-7.0.0 \
    && apt autoremove --yes -qq \
    && apt clean --yes -qq \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY intel-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/intel-env.sh" ]

CMD [ "/bin/bash" ]
