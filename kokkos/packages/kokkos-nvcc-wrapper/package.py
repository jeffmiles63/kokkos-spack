# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class KokkosNvccWrapper(CMakePackage):
    """The NVCC wrapper provides a wrapper around NVCC to make it a
       'full' C++ compiler that accepts all flags"""

    homepage = "https://github.com/kokkos/kokkos"
    git      = "https://github.com/jjwilke/kokkos-nvcc-wrapper"

    version('old',    branch='old-behavior')
    version('master', branch='master')

    variant("mpi", default=True, description="use with MPI as the underlying compiler")
    depends_on("cuda")
    depends_on("mpi", when="+mpi")
    
    def cmake_args(self):
      options = [
       "-DCMAKE_CXX_COMPILER=%s" % os.environ["SPACK_CXX"],
       "-DCMAKE_CUDA_HOST_COMPILER=%s" % os.environ["SPACK_CXX"],
       "-DCMAKE_C_COMPILER=%s" % os.environ["SPACK_CC"],
      ]
      return options

    def setup_dependent_build_environment(self, env, dependent_spec):
        wrapper = join_path(self.prefix.bin, "nvcc_wrapper")
        env.set('MPICH_CXX', wrapper)
        env.set('OMPI_CXX', wrapper)
        env.set('KOKKOS_CXX', spack_cxx)

    def setup_dependent_package(self, module, dependent_spec):
        wrapper = join_path(self.prefix.bin, "nvcc_wrapper")
        self.spec.kokkos_cxx = wrapper
