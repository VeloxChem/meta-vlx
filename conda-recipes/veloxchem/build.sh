#!/usr/bin/env bash
set -ex

# clean up unwanted compiler flags
CXXFLAGS="${CXXFLAGS//-march=nocona}"
CXXFLAGS="${CXXFLAGS//-mtune=haswell}"
CXXFLAGS="${CXXFLAGS//-march=core2}"
CXXFLAGS="${CXXFLAGS//-mssse3}"

# conda-forge's libc++ headers mark newer C++ features as unavailable for the
# deployment target, although conda-forge ships its own modern libcxx runtime
# that provides them. Needed for std::from_chars(double). See
# https://conda-forge.org/docs/maintainer/knowledge_base/#newer-c-features-with-old-sdk
if [[ "${target_platform}" == osx-* ]]; then
  CXXFLAGS="${CXXFLAGS} -D_LIBCPP_DISABLE_AVAILABILITY"
fi

# configure!
cmake \
    --log-level=DEBUG \
    -S"${SRC_DIR}" \
    -Bbuild \
    -GNinja \
    -DCMAKE_BUILD_TYPE:STRING=Release \
    -DCMAKE_INSTALL_PREFIX:PATH="${PREFIX}" \
    -DCMAKE_CXX_COMPILER:STRING="${CXX}" \
    -DENABLE_ARCH_FLAGS:BOOL=OFF \
    -DENABLE_COMMIT_HASH:BOOL=ON \
    -DPython_EXECUTABLE:STRING="${PYTHON}" \
    -DPYMOD_INSTALL_FULLDIR:PATH="${SP_DIR#$PREFIX/}/veloxchem"

# build!
cmake --build build --parallel "${CPU_COUNT}" -- -d stats

# test!
# skip unit tests

# install!
cmake --build build --target install

# Copy license files
LICENSE_DIR="${PREFIX}/share/licenses/veloxchem"
mkdir -p "${LICENSE_DIR}"
cp "${SRC_DIR}"/LICENSE* "${LICENSE_DIR}/"
