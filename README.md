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
    2.7.00     https://github.com/kokkos/kokkos/archive/2.7.00.tar.gz

Safe versions:  
    develop    [git] https://github.com/kokkos/kokkos.git
    2.7.00     https://github.com/kokkos/kokkos/archive/2.7.00.tar.gz
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
    kokkos_arch []                    Kepler30, Kepler32,     Set the architecture to
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
    qthreads [off]                    True, False             enable Qthreads backend
    serial [off]                      True, False             enable Serial backend
                                                              (default)

Installation Phases:
    cmake    build    install

Build Dependencies:
    cmake
    cuda
    hwloc
    qthreads

Link Dependencies:
    cuda
    hwloc
    qthreads

Run Dependencies:
    None

Virtual Packages: 
    None
````

## Common Kokkos Examples
Coming soon

## Setting Up Kokkos Tutorials
Coming soon

## Kokkos Kernels (and other dependent projects)
Coming soon

## NVCC Wrapper
Coming soon



