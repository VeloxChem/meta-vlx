FROM ghcr.io/enccs/meta-vlx/vlx-ci_ubuntu-20.04:sha-a72e0dd

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
    && apt autoremove --yes -qq \
    && apt clean --yes -qq \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install meson \
    && curl -Ls https://github.com/grimme-lab/xtb/archive/refs/tags/v6.5.0.tar.gz | tar xz \
    && cd xtb-6.5.0 \
    && FC=gfortran CC=gcc /usr/local/bin/meson setup build --buildtype=release -Dla_backend=openblas \
    && ninja -C build install &> /dev/null \
    && cd .. \
    && python -m pip uninstall meson \
    && rm -rf xtb-6.5.0

COPY gnu-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/gnu-env.sh" ]

CMD [ "/bin/bash" ]
