# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class KokkosKernelsTutorial(CMakePackage):
    """Kokkos Kernels provides math kernels, often BLAS or LAPACK
    for small matrices, that can be used in larger Kokkos parallel routines"""

    homepage = "https://github.com/kokkos/kokkos-kernels"
    git      = "https://github.com/kokkos/kokkos-kernels.git"

    version('diy',     branch='develop')

    backends = {
      'serial'    : (True,  "enable Serial backend (default)"),
      'cuda'      : (False, "enable Cuda backend"),
      'openmp'    : (False, "enable OpenMP backend",)
    }

    depends_on("kokkos-kernels@develop")
    for backend in backends:
      deflt, descr = backends[backend]
      variant(backend.lower(), default=deflt, description=descr)
      depends_on("kokkos-kernels+%s" % backend.lower(), when="+%s" % backend.lower())

    etis = {
      "double"                : (True,   "ETI doubles"),
      "float"                 : (False,  "ETI float"),
      "complex_double"        : (False,  "ETI complex double precision"),
      "complex_float"         : (False,  "ETI complex single precision"),
      "execspace_cuda"        : ('auto', ""),
      "memspace_cudauvmspace" : ('auto', ""),
      "memspace_cudaspace"    : ('auto', ""),
      "memspace_hostspace"    : (True,   ""),
      "execspace_openmp"      : ('auto', ""),
      "execspace_threads"     : ('auto', ""),
      "execspace_serial"      : ('auto', ""),
      "layoutleft"            : (True,   ""),
      "layoutright"           : (False,  ""),
      "ordinal_int"           : (True,   ""),
      "ordinal_int64_t"       : (False,  ""),
      "offset_int"            : (True,   ""),
      "offset_size_t"         : (True,   ""),
    }
    for eti in etis:
      deflt, descr = etis[eti]
      if deflt == "auto":
        depends_on("kokkos-kernels %s=True" % eti, when="%s=True" % eti)
        depends_on("kokkos-kernels %s=False" % eti, when="%s=False" % eti)
      else:
        depends_on("kokkos-kernels+%s" % eti, when="+%s" % eti)
        depends_on("kokkos-kernels~%s" % eti, when="~%s" % eti)

    tpls = {
      "blas"      : (False, "Link to system BLAS"),
      "mkl"       : (False, "Link to system MKL"),
      "cublas"    : (False, "Link to CUDA BLAS library"),
      "cusparse"  : (False, "Link to CUDA sparse library"),
    }
    for tpl in tpls:
      deflt, descr = tpls[tpl]
      variant(tpl, default=deflt, description=descr)
      depends_on("kokkos-kernels+%s" % tpl, when="+%s" % tpl)

    def cmake_args(self):
      spec = self.spec
      options = []

      options.append("-DKokkosKernels_ROOT=%s" % spec["kokkos-kernels"].prefix)
      return options

