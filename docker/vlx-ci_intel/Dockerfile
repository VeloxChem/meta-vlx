FROM ghcr.io/enccs/meta-vlx/vlx-ci_ubuntu-20.04:sha-99d965c

LABEL org.opencontainers.image.description "Intel-based VeloxChem CI container"

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
    && python -m pip install meson > /dev/null 2>&1 \
    && curl -Ls https://github.com/grimme-lab/xtb/archive/refs/tags/v6.5.0.tar.gz | tar xz \
    && cd xtb-6.5.0 \
    && . /opt/intel/oneapi/setvars.sh \
    && FC=ifort CC=icc /usr/local/bin/meson setup build --buildtype=release -Dfortran_args=-qopenmp > /dev/null 2>&1 \
    && ninja -C build install > /dev/null 2>&1 \
    && cd .. \
    && python -m pip uninstall --yes meson > /dev/null 2>&1 \
    && rm -rf xtb-6.5.0 \
    && apt autoremove --yes -qq \
    && apt clean --yes -qq \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY intel-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/intel-env.sh" ]

CMD [ "/bin/bash" ]
