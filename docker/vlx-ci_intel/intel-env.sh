#!/usr/bin/env bash

printf "default=exclude\nmkl=latest\nmpi=latest\ncompiler=latest\nintelpython=latest\n" > config.txt
source /opt/intel/oneapi/setvars.sh --config=config.txt

export CC=icc
export MPICC=mpiicc

export GTESTLIB="/usr/lib/x86_64-linux-gnu"

exec "$@"