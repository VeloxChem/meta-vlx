#!/usr/bin/env bash

printf "default=exclude\n" > config.txt
source /opt/intel/oneapi/setvars.sh --config=config.txt

export CC=gcc
export MPICC=mpicc
