#!/usr/bin/env bash
set -ex

# clean up unwanted compiler flags
CXXFLAGS="${CXXFLAGS//-march=nocona}"
CXXFLAGS="${CXXFLAGS//-mtune=haswell}"
CXXFLAGS="${CXXFLAGS//-march=core2}"
CXXFLAGS="${CXXFLAGS//-mssse3}"

# configure!
cmake \
    -S"${SRC_DIR}" \
    -Bbuild \
    -GNinja \
    -DCMAKE_BUILD_TYPE:STRING=Release \
    -DCMAKE_INSTALL_PREFIX:PATH="${PREFIX}" \
    -DCMAKE_CXX_COMPILER:STRING="${CXX}" \
    -DENABLE_ARCH_FLAGS:BOOL=OFF \
    -DMTP_LA_VENDOR:STRING="Generic" \
    -DPython_EXECUTABLE:STRING="${PYTHON}" \
    -DPYMOD_INSTALL_FULLDIR:PATH="${SP_DIR#$PREFIX/}/multipsi"

# build!
#cmake --build build --parallel "${CPU_COUNT}" -- -v -d stats

# integration tests are run later on with pytest

# install!
#cmake --build build --target install

SKBUILD_CONFIGURE_OPTIONS="-DMTP_LA_VENDOR=Generic -DCMAKE_CXX_COMPILER=${CXX}" \
    CMAKE_ARGS="-DCMAKE_BUILD_TYPE:STRING=Release -DENABLE_ARCH_FLAGS:BOOL=OFF" \
    ${PYTHON} -m pip install --prefix=${PREFIX} --no-build-isolation -v .

cp -r tests/ "${SP_DIR}/multipsi"
