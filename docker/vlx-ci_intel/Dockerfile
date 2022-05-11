FROM ghcr.io/enccs/meta-vlx/vlx-ci_ubuntu-20.04:sha-e0f7c31

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
    && rm -rf /var/lib/apt/lists/*

COPY intel-env.sh /opt/docker/etc

ENTRYPOINT [ "/opt/docker/etc/intel-env.sh" ]

CMD [ "/bin/bash" ]
