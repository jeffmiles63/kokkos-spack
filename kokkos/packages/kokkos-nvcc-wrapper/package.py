# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class KokkosNvccWrapper(CMakePackage):
    """The NVCC wrapper provides a wrapper around NVCC to make it a
       'full' C++ compiler that accepts all flags"""

    homepage = "https://github.com/kokkos/kokkos"
    git      = "git@github.com:jjwilke/kokkos-nvcc-wrapper.git"

    version('master', branch='master')

    depends_on("cuda")
    
    def cmake_args(self):
	import os
	options = [ 
	 "-DCMAKE_CXX_COMPILER=%s" % os.environ["SPACK_CXX"],
	 "-DCMAKE_CUDA_HOST_COMPILER=%s" % os.environ["SPACK_CXX"],
	 "-DCMAKE_C_COMPILER=%s" % os.environ["SPACK_CC"],
	]
	return options

