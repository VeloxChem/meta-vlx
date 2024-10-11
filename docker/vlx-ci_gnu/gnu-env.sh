#!/usr/bin/env bash

export CC=gcc
export MPICC=mpicc

export OPENBLAS_INCLUDE_DIR="/usr/include/x86_64-linux-gnu/openblas-openmp"
export OPENBLAS_LIBRARY="/usr/lib/x86_64-linux-gnu/openblas-openmp"
export GTESTLIB="/usr/lib/x86_64-linux-gnu"
export XTBHOME="/usr/local"
export LibXC_DIR="/usr/local/lib/cmake/Libxc"

exec "$@"
