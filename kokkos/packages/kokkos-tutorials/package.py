# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class KokkosTutorials(CMakePackage,CudaPackage):
    """Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms."""

    homepage = "https://github.com/kokkos/kokkos-tutorials"
    git      = "https://github.com/kokkos/kokkos-tutorials.git"

    version("master",  branch="master", preferred=True)

    depends_on("kokkos")

    def cmake_args(self):
      spec = self.spec
      options = []
      options.append("-DKokkos_ROOT=%s/lib64/cmake/Kokkos/" % spec["kokkos"].prefix)
      return options

