# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class KokkosKernels(CMakePackage,CudaPackage):
    """Kokkos Kernels provides math kernels, often BLAS or LAPACK
    for small matrices, that can be used in larger Kokkos parallel routines"""

    homepage = "https://github.com/kokkos/kokkos-kernels"
    git      = "https://github.com/kokkos/kokkos-kernels.git"

    version('develop', branch='develop')
    version('cmake', branch='cmake-overhaul')

    backends = {
      'serial'    : (False,  "enable Serial backend (default)"),
      'cuda'      : (False, "enable Cuda backend"),
      'openmp'    : (False, "enable OpenMP backend"),
    }

    variant("diy", default=False, description="Add necessary flags for Spack DIY mode")

    depends_on("kokkos")
    for backend in backends:
      deflt, descr = backends[backend]
      variant(backend.lower(), default=deflt, description=descr)
      depends_on("kokkos+%s" % backend.lower(), when="+%s" % backend.lower())
    depends_on("kokkos@develop", when="@develop")

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
      variant(eti, default=deflt, description=descr)

    tpls = {
      "blas"      : (False, "Link to system BLAS"),
      "mkl"       : (False, "Link to system MKL"),
      "cublas"    : (False, "Link to CUDA BLAS library"),
      "cusparse"  : (False, "Link to CUDA sparse library"),
    }
    for tpl in tpls:
      deflt, descr = tpls[tpl]
      variant(tpl, default=deflt, description=descr)

    def cmake_args(self):
      spec = self.spec
      options = []

      isDiy = "+diy" in spec
      if isDiy:
        options.append("-DSpack_WORKAROUND=On")

      options.append("-DKokkos_ROOT=%s" % spec["kokkos"].prefix)

      #atLeastOneBackend = False
      #for be in self.backends:
      #  flag = "+%s" % be.lower()
      #  if flag in self.spec:
      #    atLeastOneBackend = True
      #if not atLeastOneBackend:
      #  raise Exception("Need at least one Kokkos backend specified")

      if self.run_tests:
        options.append("-DKokkosKernels_ENABLE_TESTS=ON")

      for tpl in self.tpls:
        onFlag = "+%s" % tpl
        offFlag = "~%s" % tpl
        if onFlag in self.spec:
          options.append("-DKokkosKernels_ENABLE_TPL_%s=ON" % tpl.upper())
        elif offFlag in self.spec:
          options.append("-DKokkosKernels_ENABLE_TPL_%s=OFF" % tpl.upper())
        
      for eti in self.etis:
        deflt, descr = self.etis[eti]
        if deflt == "auto":
          value = spec.variants[eti].value
          if str(value) == "True": #spack does these as strings, not reg booleans
            options.append("-DKokkosKernels_INST_%s=ON" % eti.upper())
          elif str(value) == "False":
            options.append("-DKokkosKernels_INST_%s=OFF" % eti.upper())
          else:
            pass #don't pass anything, let CMake decide
        else: #simple option
          onFlag = "+%s" % eti
          offFlag = "~%s" % eti
          if onFlag in self.spec:
            options.append("-DKokkosKernels_INST_%s=ON" % eti.upper())
          elif offFlag in self.spec:
            options.append("-DKokkosKernels_INST_%s=OFF" % eti.upper())

      return options

