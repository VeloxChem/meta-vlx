"""Preflight check that mpi4py initializes correctly under mpiexec."""

from mpi4py import MPI

print("MPI library:", MPI.Get_library_version().splitlines()[0])
print("MPI size:", MPI.COMM_WORLD.Get_size())
