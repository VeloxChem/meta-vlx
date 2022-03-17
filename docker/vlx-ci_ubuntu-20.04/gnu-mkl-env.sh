#!/usr/bin/env bash

printf "default=exclude\nmkl=latest\n" > config.txt
source /opt/intel/oneapi/setvars.sh --config=config.txt

export CC=gcc
export MPICC=mpicc
