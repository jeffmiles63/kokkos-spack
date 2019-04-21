# Kokkos Spack Repository

This repo will be the most up-to-date location for Spack packages for Kokkos and Kokkos Kernels.

## Getting Started

Make sure you have downloaded [Spack](https://github.com/spack/spack) and added it to your path.
The easiest way to do this is often (depending on your SHELL):
````
source spack/share/spack/setup-env.sh 
````

After downloading the kokkos-spack GitHub repository, you simply need to run
````
spack repo add kokkos-spack/kokkos
````

To validate that Spack now sees the repo with the Kokkos packages, run:
````
spack repo list
````
This should now list your newly downloaded Spack repo.
You can display information about how to install the packages with:
````
spack info kokkos
````
This will print all the information about how to install Kokkos with Spack.
For detailed instructions on how to use Spack, see the [Owner's Manual](https://spack.readthedocs.io).
````
CMakePackage:   kokkos

Description:
    Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms.

Homepage: https://github.com/kokkos/kokkos

Tags: 
    None

Preferred version:  
    2.8.00     https://github.com/kokkos/kokkos/archive/2.8.00.tar.gz

Safe versions:  
    develop    [git] https://github.com/kokkos/kokkos.git
    2.8.00     https://github.com/kokkos/kokkos/archive/2.8.00.tar.gz
    master     [git] https://github.com/kokkos/kokkos.git
    cmake      [git] https://github.com/kokkos/kokkos.git

Variants:
    Name [Default]                    Allowed values          Description


    aggressive_vectorization [off]    True, False             set aggressive_vectorization
                                                              Kokkos option
    build_type [RelWithDebInfo]       Debug, Release,         CMake build type
                                      RelWithDebInfo,         
                                      MinSizeRel              
    compiler_warnings [off]           True, False             turn on verbose
                                                              compiler_warnings
    cuda [off]                        True, False             enable Cuda backend
    cuda_lambda [off]                 True, False             Enable experimental Lambda
                                                              featuers
    cuda_ldg_intrinsic [off]          True, False             Use LDG intrinstics for read-
                                                              only caching
    cuda_rdc [off]                    True, False             Compile for relocatable device
                                                              code
    cuda_uvm [off]                    True, False             Force data structures to use
                                                              UVM by default for CUDA
    deprecated_code [off]             True, False             activates old, deprecated code
                                                              (please don't use)
    eti [off]                         True, False             set enable_eti Kokkos option
    kokkos_arch [None]                Kepler30, Kepler32,     Set the architecture to
                                      Kepler35, Kepler37,     optimize for
                                      Maxwell50,              
                                      Maxwell52,              
                                      Maxwell53, Pascal60,    
                                      Pascal61, Volta70,      
                                      Volta72, AMDAVX,        
                                      ARMv80, ARMv81,         
                                      ARMv8-ThunderX,         
                                      Power7, Power8,         
                                      Power9, WSM, SNB,       
                                      HSW, BDW, SKX, KNC,     
                                      KNL                     
    openmp [off]                      True, False             enable OpenMP backend
    pic [off]                         True, False             enable position independent
                                                              code (-fPIC flag)
    profiling [off]                   True, False             activate binding for Kokkos
                                                              profiling tools
    profiling_load_print [off]        True, False             set enable_profile_load_print
                                                              Kokkos option
    serial [off]                      True, False             enable Serial backend
                                                              (default)

Installation Phases:
    cmake    build    install

Build Dependencies:
    cmake
    cuda
    hwloc

Link Dependencies:
    cuda
    hwloc
````

## Setting Up Spack: Avoiding the Package Cascade
By default, Spack doesn't 'see' anything on your system - including things like CMake and CUDA.
At minimum, we recommend adding a `packages.yaml` to your `$HOME.spack` folder that includes CMake (and CUDA, if applicable).  For example, your `packages.yaml` file could be:
````
packages:
 cuda:
  modules:
   cuda@9.2.88: [cuda/9.2.88]
  paths:
   cuda@9.2.88:
    /opt/local/ppc64le-pwr8-nvidia/cuda/9.2.88
  buildable: false
 cmake:
  modules:
   cmake: [cmake]
  paths:
   cmake:
    /opt/local/ppc64le/cmake/3.9.6
  buildable: false
````
The `modules` entry is only necessary on systems that require loading Modules (i.e. most DOE systems).
The `buildable` flag is useful to make sure Spack crashes if there is a path error, 
rather than having a type-o and Spack rebuilding everything because `cmake` isn't found.
You can verify your environment is set up correctly by running `spack graph`. 
For example:
````
spack graph kokkos +cuda
o  kokkos
|\
o |  cuda
 /
o  cmake
````
Without the existing CUDA and CMake being identified in `packages.yaml`, a (subset!) of the output would be:
````
o  kokkos
|\
| o  cmake
| |\
| | | |\
| | | | | |\
| | | | | | | |\
| | | | | | | | | |\
| | | | | | | o | | |  libarchive
| | | | | | | |\ \ \ \
| | | | | | | | | |\ \ \ \
| | | | | | | | | | | | |_|/
| | | | | | | | | | | |/| |
| | | | | | | | | | | | | o  curl
| | |_|_|_|_|_|_|_|_|_|_|/|
| |/| | | |_|_|_|_|_|_|_|/
| | | | |/| | | | | | | |
| | | | o | | | | | | | |  openssl
| |/| | | | | | | | | | |
| | | | | | | | | | o | |  libxml2
| | |_|_|_|_|_|_|_|/| | |
| | | | | | | | | | |\ \ \
| o | | | | | | | | | | | |  zlib
|  / / / / / / / / / / / /
| o | | | | | | | | | | |  xz
|  / / / / / / / / / / /
| o | | | | | | | | | |  rhash
|  / / / / / / / / / /
| | | | o | | | | | |  nettle
| | | | |\ \ \ \ \ \ \
| | | o | | | | | | | |  libuv
| | | | o | | | | | | |  autoconf
| | |_|/| | | | | | | |
| | | | |/ / / / / / /
| o | | | | | | | | |  perl
| o | | | | | | | | |  gdbm
| o | | | | | | | | |  readline
````

## NVCC Wrapper
Kokkos is a C++ project, but often builds for the CUDA backend. This is particularly problematic with CMake. At this point, `nvcc` does not accept all the flags that normally get passed to a C++ compiler.  Kokkos provides `nvcc_wrapper` that identifies correctly as a C++ compiler to CMake and accepts C++ flags, but uses `nvcc` as the underlying compiler.

Adding `nvcc_wrapper` as a valid compiler in the Spack toolchain requires a few steps, but is straightforward.
First, you must install the Spack package using the correct underlying compiler. In this example we use GCC 7.2.
````
spack install kokkos-nvcc-wrapper %gcc@7.2.0
````
After installing, locate the path to the compiler by running:
````
spack find -p kokkos-nvcc-wrapper %gcc@7.2.0
````
Spack maintains a list of valid compilers in its `compilers.yaml` file, usually found at `$HOME/.spack`.
There should already exist an entry in this file for the compiler (e.g. GCC 7.2) you used to build `nvcc_wrapper`.
Copy this entry and modify slightly, changing the compiler name (e.g. `gcc@7.2.0-kokkos`) and the C++ compiler path:
````
- compiler:
    modules: [gcc/7.2.0]
    operating_system: rhel7
    paths:
      cc: /opt/local/bin/gcc
      f77: /opt/local/bin/gfortran
      fc: /opt/local/bin/gfortran
      cxx: /projects/linux-rhel7-ppc64le/gcc-7.2.0/kokkos-nvcc-wrapper-master-skz642na6cvjxl2hhunauewk6haqyu5u/bin/nvcc_wrapper
    spec: gcc@7.2.0-kokkos
    target: ppc64le
````
You can now build Kokkos (and Kokkos-dependent projects) using this compiler with the CUDA backend, e.g.
````
spack install kokkos +cuda %gcc@7.2.0-kokkos
````

## Common Kokkos Examples
Kokkos backends are Spack variants, specified with the `+` syntax. Most of these variants are listed above in the `spack info` output.  Spack will choose a default compiler, if none is specified using the `%` syntax. For Kokkos, best practice is to always choose a specific compiler for Kokkos.
````
spack insall kokkos +cuda +serial kokkos_arch=Volta70 %gcc@7.2.0-kokkos
````
The given spec builds the CUDA backend with serial support, using an installed `nvcc_wrapper` as the underlying compiler. In this case, Kokkos should optimize for the Volta 7.0 architecture. Another possibility is
````
spack install kokoks +openmp kokkos_arch=HSW %intel@18
````
which builds the OpenMP backend, optimized for Haswell using an Intel 18 compiler. 

Spack variants not only specify backends, but can activate certain features. The most common are explicit template instantation (`+eti`) and the Kokkos profiling tools (`+profiling`).
````
spack install kokkos +openmp +profiling +eti kokkos_arch=HSW  %intel@18
````

## Setting Up Kokkos Tutorials
Coming soon

## Kokkos Kernels (and other dependent projects)
Coming soon






