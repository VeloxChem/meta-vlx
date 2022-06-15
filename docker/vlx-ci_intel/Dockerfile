FROM ghcr.io/enccs/meta-vlx/vlx-ci_ubuntu-20.04:sha-a72e0dd

# add a timestamp for the build. Also, bust the cache.
ADD http://worldclockapi.com/api/json/utc/now /opt/docker/etc/timestamp

# install software
RUN apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -qq \
       -o Dpkg::Options::="--force-confnew" \
       intel-oneapi-compiler-dpcpp-cpp-and-cpp-classic \
       intel-oneapi-mkl \
       intel-oneapi-mkl-devel \
       intel-oneapi-mpi \
       intel-oneapi-mpi-devel \
       intel-oneapi-openmp \
    && apt autoremove --yes -qq \
    && apt clean --yes -qq \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install meson > /dev/null 2>&1 \
    && curl -Ls https://github.com/grimme-lab/xtb/archive/refs/tags/v6.5.0.tar.gz | tar xz \
    && cd xtb-6.5.0 \
    && FC=ifort CC=icc /usr/local/bin/meson setup build --buildtype=release > /dev/null 2>&1 \
    && ninja -C build install &> /dev/null \
    && cd .. \
    && python -m pip uninstall meson \
    && rm -rf xtb-6.5.0

COPY intel-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/intel-env.sh" ]

CMD [ "/bin/bash" ]
