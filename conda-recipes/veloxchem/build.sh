#!/usr/bin/env bash
set -ex

# configure
$PYTHON ${SRC_DIR}/config/generate_setup.py

# build
env VERBOSE=1 make -C ${SRC_DIR}/src release -j ${CPU_COUNT}
env VERBOSE=1 make -C ${SRC_DIR}/unit_tests release -j ${CPU_COUNT}

# test
# unit tests
${SRC_DIR}/build/bin/UnitTestVeloxChem.x

# install
cp -r ${SRC_DIR}/build/lib/veloxchem ${SP_DIR}
