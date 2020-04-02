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

    version('3.0',     url='https://github.com/kokkos/kokkos-kernels/archive/3.0.00.tar.gz',
            sha256="e4b832aed3f8e785de24298f312af71217a26067aea2de51531e8c1e597ef0e6")
    version('develop', branch='develop')
    version('master',  branch='master')

    depends_on("kokkos")
    depends_on("kokkos@develop", when="@develop")

    backends = {
      'serial'    : (False,  "enable Serial backend (default)"),
      'cuda'      : (False,  "enable Cuda backend"),
      'openmp'    : (False,  "enable OpenMP backend"),
    }

    for backend in backends:
      deflt, descr = backends[backend]
      variant(backend.lower(), default=deflt, description=descr)
      depends_on("kokkos+%s" % backend.lower(), when="+%s" % backend.lower())

    space_etis = {
      "execspace_cuda"        : ('auto', ""),
      "execspace_openmp"      : ('auto', ""),
      "execspace_threads"     : ('auto', ""),
      "execspace_serial"      : ('auto', ""),
      "memspace_cudauvmspace" : ('auto', ""),
      "memspace_cudaspace"    : ('auto', ""),
    }
    for eti in space_etis:
      deflt, descr = space_etis[eti]
      variant(eti, default=deflt, description=descr)

    numeric_etis = {
      "ordinals" : ("int",        "ORDINAL_", #default, cmake name
                    ["int", "int64_t"]),      #allowed values
      "offsets"  : ("int,size_t", "OFFSET_",
                    ["int", "size_t"]),
      "layouts"  : ("left",       "LAYOUT",
                    ["left", "right"]),
      "scalars"  : ("double",     "",
                    ["float", "double", "complex_float", "complex_double"])
    }
    for eti in numeric_etis:
      deflt, cmake_name, vals = numeric_etis[eti]
      variant(eti, default=deflt, values=vals, multi=True)

    tpls = {
      #variant name   #deflt   #spack name   #root var name #docstring
      "blas"         : (False, "blas",       "BLAS",        "Link to system BLAS"),
      "lapack"       : (False, "lapack",     "LAPACK",      "Link to system LAPACK"),
      "mkl"          : (False, "mkl",        "MKL",         "Link to system MKL"),
      "cublas"       : (False, "cuda",       None,          "Link to CUDA BLAS library"),
      "cusparse"     : (False, "cuda",       None,          "Link to CUDA sparse library"),
      "superlu"      : (False, "superlu",    "SUPERLU",     "Link to SuperLU library"),
      "cblas"        : (False, "cblas",      "CBLAS",       "Link to CBLAS library"),
      "lapacke"      : (False, "clapack",    "LAPACKE",     "Link to LAPACKE library"),
    }

    for tpl in tpls:
      deflt, spackName, rootName, descr = tpls[tpl]
      variant(tpl, default=deflt, description=descr)
      depends_on(spackName, when="+%s" % tpl)

    def cmake_args(self):
      spec = self.spec
      options = []

      isDiy = "+diy" in spec
      if isDiy:
        options.append("-DSpack_WORKAROUND=On")

      options.append("-DKokkos_ROOT=%s" % spec["kokkos"].prefix)
      # Compiler weirdness due to nvcc_wrapper
      options.append("-DCMAKE_CXX_COMPILER=%s" % spec["kokkos"].kokkos_cxx)

      if self.run_tests:
        options.append("-DKokkosKernels_ENABLE_TESTS=ON")

      for tpl in self.tpls:
        onFlag = "+%s" % tpl
        offFlag = "~%s" % tpl
        dflt, spackName, rootName, descr = self.tpls[tpl]
        if onFlag in self.spec:
          options.append("-DKokkosKernels_ENABLE_TPL_%s=ON" % tpl.upper())
          if rootName:
            options.append("-D%s_ROOT=%s" % (rootName, spec[spackName].prefix))
          else:
            pass #this should get picked up automatically, we hope
        elif offFlag in self.spec:
          options.append("-DKokkosKernels_ENABLE_TPL_%s=OFF" % tpl.upper())

      for eti in self.numeric_etis:
        deflt, cmake_name, vals = self.numeric_etis[eti]
        for val in vals:
          keyval = "%s=%s" % (eti, val)
          cmake_option = "KokkosKernels_INST_%s%s" % (cmake_name.upper(), val.upper())
          if keyval in spec:
            options.append("-D%s=ON" % cmake_option)
          else:
            options.append("-D%s=OFF" % cmake_option)
        
      for eti in self.space_etis:
        deflt, descr = self.space_etis[eti]
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

