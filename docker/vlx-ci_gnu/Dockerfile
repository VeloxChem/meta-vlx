FROM ghcr.io/enccs/meta-vlx/vlx-ci_ubuntu-20.04:latest

# add a timestamp for the build. Also, bust the cache.
ADD http://worldclockapi.com/api/json/utc/now /opt/docker/etc/timestamp

# install software
RUN apt update --yes -qq \
    && DEBIAN_FRONTEND=noninteractive apt install --yes -o Dpkg::Options::="--force-confnew" -qq \
       g++ \
       gcc \
       libopenblas-dev \
       libopenblas-openmp-dev \
       libopenmpi-dev \
       libpython3-dev \
       openmpi-bin \
       python-is-python3 \
       python3 \
       python3-pip \
       python3-venv \
    && apt clean --yes -qq \
    && rm -rf /var/lib/apt/lists/*

COPY gnu-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/gnu-env.sh" ]

CMD [ "/bin/bash" ]
