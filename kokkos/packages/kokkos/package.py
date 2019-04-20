# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kokkos(CMakePackage):
    """Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms."""

    homepage = "https://github.com/kokkos/kokkos"
    url      = "https://github.com/kokkos/kokkos/archive/2.03.00.tar.gz"
    git      = "https://github.com/kokkos/kokkos.git"

    version('develop', branch='develop')
    version('master', branch='master')
    version('cmake', branch='cmake-overhaul')
    version('2.7.00',  'b357f9374c1008754babb4495f95e392')

    
    variant('serial', default=True, description="enable Serial backend (default)")
    nondefault_backends = {
      'serial'    : "enable Serial backend (default)",
      'qthreads'  : "enable Qthreads backend",
      'cuda'      : "enable Cuda backend",
      'openmp'    : "enable OpenMP backend",
    }
    for backend in nondefault_backends:
      variant(backend, default=False, description=nondefault_backends[backend])
    backends = nondefault_backends.keys() + ["serial"]

    universal_variants = {
      'PIC'                           : "enable position independent code (-fPIC flag)",
      'Aggressive_Vectorization'      : "set aggressive_vectorization Kokkos option",
      'Profiling'                     : "activate binding for Kokkos profiling tools",
      'Profiling_Load_Print'          : "set enable_profile_load_print Kokkos option",
      'Compiler_Warnings'             : "turn on verbose compiler_warnings",
      'Deprecated_Code'               : "activates old, deprecated code (please don't use)",
      'ETI'                           : "set enable_eti Kokkos option",
    }

    for var in universal_variants:
      variant(var.lower(), default=False, description=universal_variants[var])

    gpu_values = ('Kepler30', 'Kepler32', 'Kepler35', 'Kepler37',
                  'Maxwell50', 'Maxwell52', 'Maxwell53',
                  'Pascal60', 'Pascal61',
                  'Volta70', 'Volta72')
    host_values =  ('AMDAVX', 'ARMv80', 'ARMv81', 'ARMv8-ThunderX',
                  'Power7', 'Power8', 'Power9',
                  'WSM', 'SNB', 'HSW', 'BDW', 'SKX', 'KNC', 'KNL')
    arch_values = gpu_values + host_values
    # Architecture to optimize for
    variant(
        'kokkos_arch',
        default=None,
        values=arch_values,
        description='Set the architecture to optimize for'
    )

    cuda_variants = {
      'UVM'             : "Force data structures to use UVM by default for CUDA",
      'LDG_Intrinsic'   : "Use LDG intrinstics for read-only caching",
      'RDC'             : "Compile for relocatable device code",
      'Lambda'          : "Enable experimental Lambda featuers",
    }
    for opt in cuda_variants: #add as a lowercase option
      variant("cuda_%s" % opt.lower(), default=False,
              description=cuda_variants[opt])

    # Check that we haven't specified a gpu architecture
    # without specifying CUDA
    for p in gpu_values:
        conflicts('gpu_arch={0}'.format(p), when='~cuda',
            msg='Must specify CUDA backend to use a GPU architecture.')

    for opt in cuda_variants:
      conflicts('+%s' % opt, when="~cuda", msg="Must enable CUDA to use %s" % opt)

    # Check that we haven't asked for a GPU architecture that
    # the revision of kokkos does not support
    conflicts('arch=Volta70', when='@:2.5.99')
    conflicts('arch=Volta72', when='@:2.5.99')

    # conflicts on kokkos version and cuda enabled
    # see kokkos issue #1296
    # https://github.com/kokkos/kokkos/issues/1296
    conflicts('+cuda', when='@2.5.00:develop',
        msg='Kokkos build system has issue when CUDA enabled'
        ' in version 2.5.00 through 2.7.00, and develop until '
        'issue #1296 is resolved.')

    # Specify that v1.x is required as v2.x has API changes
    depends_on('hwloc', when="+hwloc")
    depends_on('qthreads', when='+qthreads')
    depends_on('cuda', when='+cuda')

    def append_enables(self, options, enable_list, prefix=""):
      for enabled in enable_list:
        var = enabled
        if prefix:
          var = prefix + var
        options.append("-DKOKKOS_ENABLE_%s=ON" % var)
        
  
    def cmake_args(self):
      spec = self.spec
      options = []

      if spec.variants["kokkos_arch"].value:
        options.append("-DKOKKOS_ARCH=%s" % spec.variants["kokkos_arch"].value)

      for tpl in "hwloc", "qthreads":
        specStr = "+%s" % tpl
        if specStr in spec:
          options.append("-DKOKKOS_ENABLE_%s=ON" % tpl.upper())
          options.append("-D%s_DIR=%s" % (tpl, specs[tpl].prefix))

      self.append_enables(options, self.universal_variants)
      self.append_enables(options, self.cuda_variants, "Cuda_")
      self.append_enables(options, self.backends)

      return options

