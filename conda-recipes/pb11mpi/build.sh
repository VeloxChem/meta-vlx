#!/usr/bin/env bash
set -ex

# configure!
cmake \
    -S"${SRC_DIR}" \
    -Bbuild \
    -GNinja \
    -DCMAKE_BUILD_TYPE:STRING=Release \
    -DCMAKE_INSTALL_PREFIX:PATH="${PREFIX}" \
    -DCMAKE_PREFIX_PATH:PATH="${LIBRARY_PREFIX}" \
    -DCMAKE_CXX_COMPILER:STRING="${CXX}" \
    -DPython_EXECUTABLE:STRING="${PYTHON}" \
    -DPYMOD_INSTALL_FULLDIR:PATH="${SP_DIR#$PREFIX/}/pb11mpi"

# build!
cmake --build build --parallel ${CPU_COUNT} -- -v -d stats

# test!
cd build
ctest --output-on-failure --parallel ${CPU_COUNT}

# install!
cd ..
cmake --build build --target install
