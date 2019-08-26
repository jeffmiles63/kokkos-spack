# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class KokkosTutorial(CMakePackage):
    """Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms."""

    homepage = "https://github.com/kokkos/kokkos"
    git      = "https://github.com/kokkos/kokkos.git"

    version("cmake", branch="tutorial")

    variants = {
     'cuda'                           : [False, 'Whether to build CUDA backend'],
     'openmp'                         : [ True, 'Whether to build OpenMP backend'],
     'pthread'                        : [False, 'Whether to build Pthread backend'],
     'rocm'                           : [False, 'Whether to build AMD ROCm backend'],
     'serial'                         : [ True, 'Whether to build serial backend'],
     'hpx'                            : [False, 'Whether to enable the HPX library'],
     'hwloc'                          : [False, 'Whether to enable the HWLOC library'],
     'libnuma'                        : [False, 'Whether to enable the LIBNUMA library'],
     'memkind'                        : [False, 'Whether to enable the MEMKIND library'],
     'aggressive_vectorization'       : [False, 'Whether to aggressively vectorize loops'],
     'compiler_warnings'              : [False, 'Whether to print all compiler warnings'],
     'cuda_lambda'                    : [False, 'Whether to activate experimental laambda features'],
     'cuda_ldg_intrinsic'             : [False, 'Whether to use CUDA LDG intrinsics'],
     'cuda_relocatable_device_code'   : [False, 'Whether to enable relocatable device code (RDC) for CUDA'],
     'cuda_uvm'                       : [False, 'Whether to enable unified virtual memory (UVM) for CUDA'],
     'debug'                          : [False, 'Whether to activate extra debug features - may increase compiletimes'],
     'debug_bounds_check'             : [False, 'Whether to use bounds checking - will increase runtime'],
     'debug_dualview_modify_check'    : [False, 'Debug check on dual views'],
     'deprecated_code'                : [False, 'Whether to enable deprecated code'],
     'examples'                       : [False, 'Whether to build OpenMP  backend'],
     'explicit_instantiation'         : [False, 'Whether to explicitly instantiate certain types to lower futurecompile times'],
     'hpx_async_dispatch'             : [False, 'Whether HPX supports asynchronous dispath'],
     'profiling'                      : [ True, 'Whether to create bindings for profiling tools'],
     'profiling_load_print'           : [False, 'Whether to print information about which profiling tools gotloaded'],
     'qthread'                        : [False, 'Whether to enable the QTHREAD library'],
     'tests'                          : [False, 'Whether to build for tests'],
     'amdavx'                         : [False, 'Whether to optimize for the AMDAVX architecture'],
     'armv80'                         : [False, 'Whether to optimize for the ARMV80 architecture'],
     'armv81'                         : [False, 'Whether to optimize for the ARMV81 architecture'],
     'armv8_thunderx'                 : [False, 'Whether to optimize for the ARMV8_THUNDERX architecture'],
     'armv8_tx2'                      : [False, 'Whether to optimize for the ARMV8_TX2 architecture'],
     'bdw'                            : [False, 'Whether to optimize for the BDW architecture'],
     'bgq'                            : [False, 'Whether to optimize for the BGQ architecture'],
     'carrizo'                        : [False, 'Whether to optimize for the CARRIZO architecture'],
     'epyc'                           : [False, 'Whether to optimize for the EPYC architecture'],
     'fiji'                           : [False, 'Whether to optimize for the FIJI architecture'],
     'gfx901'                         : [False, 'Whether to optimize for the GFX901 architecture'],
     'hsw'                            : [ True, 'optimize for architecture HSW'],
     'kaveri'                         : [False, 'Whether to optimize for the KAVERI architecture'],
     'kepler'                         : [False, 'Whether to optimize for the KEPLER architecture'],
     'kepler30'                       : [False, 'Whether to optimize for the KEPLER30 architecture'],
     'kepler32'                       : [False, 'Whether to optimize for the KEPLER32 architecture'],
     'kepler35'                       : [False, 'Whether to optimize for the KEPLER35 architecture'],
     'kepler37'                       : [False, 'Whether to optimize for the KEPLER37 architecture'],
     'knc'                            : [False, 'Whether to optimize for the KNC architecture'],
     'knl'                            : [False, 'Whether to optimize for the KNL architecture'],
     'maxwell'                        : [False, 'Whether to optimize for the MAXWELL architecture'],
     'maxwell50'                      : [False, 'Whether to optimize for the MAXWELL50 architecture'],
     'maxwell52'                      : [False, 'Whether to optimize for the MAXWELL52 architecture'],
     'maxwell53'                      : [False, 'Whether to optimize for the MAXWELL53 architecture'],
     'pascal60'                       : [False, 'Whether to optimize for the PASCAL60 architecture'],
     'pascal61'                       : [False, 'Whether to optimize for the PASCAL61 architecture'],
     'power7'                         : [False, 'Whether to optimize for the POWER7 architecture'],
     'power8'                         : [False, 'Whether to optimize for the POWER8 architecture'],
     'power9'                         : [False, 'Whether to optimize for the POWER9 architecture'],
     'ryzen'                          : [False, 'Whether to optimize for the RYZEN architecture'],
     'skx'                            : [False, 'Whether to optimize for the SKX architecture'],
     'snb'                            : [ True, 'Whether to optimize for the SNB architecture'],
     'turing75'                       : [False, 'Whether to optimize for the TURING75 architecture'],
     'vega'                           : [False, 'Whether to optimize for the VEGA architecture'],
     'volta70'                        : [False, 'Whether to optimize for the VOLTA70 architecture'],
     'volta72'                        : [False, 'Whether to optimize for the VOLTA72 architecture'],
     'wsm'                            : [False, 'Whether to optimize for the WSM architecture'],
    }

    depends_on("kokkos")

    for var in variants:
      dflt, desc = variants[var]
      variant(var, default=dflt, description=desc)
      depends_on("kokkos+%s" % var, when="+%s" % var)
      depends_on("kokkos~%s" % var, when="~%s" % var)

    def cmake_args(self):
      spec = self.spec
      options = []
      options.append("-DKokkos_DIR=%s/lib/cmake/Kokkos" % spec["kokkos"].prefix)
      return options

