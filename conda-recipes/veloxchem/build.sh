#!/usr/bin/env bash
set -ex

# configure
$PYTHON ${SRC_DIR}/config/generate_setup.py

type -P mpicxx

# build
env VERBOSE=1 make -C ${SRC_DIR}/src release -j ${CPU_COUNT}
env VERBOSE=1 make -C ${SRC_DIR}/unit_tests release -j ${CPU_COUNT}

# test
# unit tests
${SRC_DIR}/build/bin/UnitTestVeloxChem.x
# integration tests
#echo "Run integration tests with OpenMP (OMP_NUM_THREADS=${CPU_COUNT})"
#env PYTHONPATH=${SRC_DIR}/build/lib:$PYTHONPATH OMP_NUM_THREADS=${CPU_COUNT} mpirun -np 1 --allow-run-as-root pytest -vv ${SRC_DIR}/python_tests/test_*.py
#
#nprocs=2
#nthreads=$(${CPU_COUNT} / ${nprocs})
#echo "Run integration tests on solvers with MPI+OpenMP (MPI processes=${nprocs}; OMP_NUM_THREADS=${nthreads})"
#for x in lr rpa cpp c6; do
#    env PYTHONPATH=${SRC_DIR}/build/lib:$PYTHONPATH OMP_NUM_THREADS=${nthreads} mpirun -np ${nprocs} --allow-run-as-root pytest -vv ${SRC_DIR}/python_tests/test_${x}.py
#done

# install
cp -r ${SRC_DIR}/build/lib/veloxchem ${SP_DIR}
