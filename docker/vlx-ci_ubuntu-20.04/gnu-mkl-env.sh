#!/usr/bin/env bash

printf "default=exclude\nmkl=latest\n" > config.txt
source /opt/intel/oneapi/setvars.sh --config=config.txt

# install mpi4py using GNU and OpenMPI
CC=gcc MPICC=mpicc python -m pip install mpi4py --no-binary=mpi4py

python -c "import mpi4py; print(mpi4py.get_config())"
