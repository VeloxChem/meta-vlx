#!/usr/bin/env bash

export CC=gcc
export MPICC=mpicc

export GTESTLIB="/usr/lib/x86_64-linux-gnu"

exec "$@"
