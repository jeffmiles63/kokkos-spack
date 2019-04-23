# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class KokkosKernels(CMakePackage):
    """Kokkos Kernels provides math kernels, often BLAS or LAPACK
    for small matrices, that can be used in larger Kokkos parallel routines"""

    homepage = "https://github.com/kokkos/kokkos-kernels"
    git      = "https://github.com/kokkos/kokkos-kernels.git"

    version('cmake', branch='cmake-overhaul')

    backends = {
      'Serial'    : (True,  "enable Serial backend (default)"),
      'CUDA'      : (False, "enable Cuda backend"),
      'OpenMP'    : (False, "enable OpenMP backend",)
    }

    depends_on("kokkos")
    for backend in backends:
      deflt, descr = backends[backend]
      variant(backend.lower(), default=deflt, description=descr)
      depends_on("kokkos+%s" % backend.lower(), when="+%s" % backend.lower())
    depends_on("kokkos@cmake", when="@cmake")

    etis = {
      "double" :         (True,  "ETI doubles"),
      "float"  :         (False, "ETI float"), 
      "complex_double" : (False, "ETI complex double precision"), 
      "complex_float"  : (False, "ETI complex single precision"),
    }
    for eti in etis:
      deflt, descr = etis[eti]
      variant(eti, default=deflt, description=descr)


    def cmake_args(self):
      spec = self.spec
      options = []

      options.append("-DKokkos_DIR=%s/lib/cmake" % spec["kokkos"].prefix)

      atLeastOneBackend = False
      for be in self.backends:
        flag = "+%s" % be.lower()
        if flag in self.spec:
          atLeastOneBackend = True
      if not atLeastOneBackend:
        raise Exception("Need at least one Kokkos backend specified")

      if self.run_tests:
        options.append("-DKokkosKernels_ENABLE_TESTS=ON")
        
      for eti in self.etis:
        if eti in self.spec:
          options.append("-DKokkosKernels_INST_%s" % eti.upper())

      return options

