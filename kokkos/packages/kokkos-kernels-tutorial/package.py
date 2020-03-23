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

    version('master',  branch='master', preferred=True)
    version('develop', branch='develop')

    depends_on("kokkos-kernels")

    def cmake_args(self):
      spec = self.spec
      options = []

      options.append("-DKokkosKernels_ROOT=%s" % spec["kokkos-kernels"].prefix)
      return options

