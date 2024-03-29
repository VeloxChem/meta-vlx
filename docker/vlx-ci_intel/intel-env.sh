#!/usr/bin/env bash

printf "default=exclude\nmkl=latest\nmpi=latest\ncompiler=latest\n" > config.txt
source /opt/intel/oneapi/setvars.sh --config=config.txt

export CC=icc
export MPICC=mpiicc

export GTESTLIB="/usr/lib/x86_64-linux-gnu"
export XTBHOME="/usr/local"
export LibXC_DIR="/usr/local/lib/cmake/Libxc"

exec "$@"
