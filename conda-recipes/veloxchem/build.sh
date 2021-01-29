#!/usr/bin/env bash
set -euxo

# configure!
cmake \
    -S${SRC_DIR} \
    -Bbuild \
    -GNinja \
    -DCMAKE_BUILD_TYPE:STRING=Release \
    -DCMAKE_INSTALL_PREFIX:PATH=${PREFIX} \
    -DCMAKE_PREFIX_PATH:PATH=${LIBRARY_PREFIX} \
    -DCMAKE_CXX_COMPILER=${CXX} \
    -DPython_EXECUTABLE=${PYTHON} \
    -DPYMOD_INSTALL_FULLDIR=${SP_DIR#$PREFIX}/veloxchem

# build!
cmake --build build --parallel ${CPU_COUNT} -- -v -d stats

# test!
# we only run unit tests here, integration tests are run later on
cd build
ctest -L unit --output-on-failure

# install!
cd ..
cmake --build build --target install
