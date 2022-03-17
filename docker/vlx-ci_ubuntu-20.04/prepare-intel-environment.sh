#!/usr/bin/env bash

printf "default=exclude\nmkl=latest\nmpi=latest\ncompiler=latest\n" > config.txt
source /opt/intel/oneapi/setvars.sh --config=config.txt

# install mpi4py using IntelMPI
CC=icx MPICC=mpiicx python -m pip install mpi4py --no-binary=mpi4py
