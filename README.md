![Kokkos](https://avatars2.githubusercontent.com/u/10199860?s=200&v=4)

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
For detailed instructions on how to use Spack, see the [User Manual](https://spack.readthedocs.io).

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

## Configuring Kokkos as a Project Dependency
Say you have a project "SuperScience" which needs to use kokkos.
In your `package.py` file, you would generally include something like:
````
class SuperScience(CMakePackage):
  ...
  depends_on("kokkos")
````
Often projects want to tweak behavior when using certain features, e.g.
````
  depends_on("kokkos+cuda", when="+cuda")
````
if your project needs CUDA-specific logic to configure and build.
This illustrates the general principle in Spack of "flowing-up".
A user requests a feature in the final app:
````
spack install superscience+cuda
````
This flows upstream to the Kokkos dependency, causing the `kokkos+cuda` variant to build.
The downstream app (SuperScience) tells the upstream app (Kokkos) how to build.

Because Kokkos is a performance portability library, it somewhat inverts this principle.
Kokkos "flows-down", telling your application how best to configure for performance.
Rather than a downstream app (SuperScience) telling the upstream (Kokkos) what variants to build,
a pre-built Kokkos should be telling the downstream app SuperScience what variants to use.
Kokkos works best when there is an "expert" configuration installed on your system.
Your build should simply request `-DKokkos_ROOT=<BEST_KOKKOS_FOR_MY_SYSTEM>` and configure appropriately based on the Kokkos it finds.

Kokkos has many, many build variants.
Where possible, projects should only depend on a general Kokkos, not specific variants.
We recommend instead adding, for each system you build on, a Kokkos configuration to your `packages.yaml` file (usually found in `~/.spack` for specific users).
For a Xeon + Volta system, this could look like:
````
 kokkos:
  variants: +cuda +openmp +volta70 +cuda_lambda +wrapper ^cuda@10.1
  compiler: [gcc@7.2.0]
````
which gives the "best" Kokkos configuration as CUDA+OpenMP optimized for a Volta 7.0 architecture using CUDA 10.1.
It also enables support for CUDA Lambdas.
The `+wrapper` option tells Kokkos to build with the special `nvcc_wrapper` (more below).
For a Haswell system, this might look like:
````
 kokkos:
  variants: +openmp +hsw
  compiler: [intel@18]
````
Without an optimal default in your `packages.yaml` file, it is highly likely that the default Kokkos configuration you get will not be what you want.
For example, CUDA is not enabled by default (there is no easy logic to conditionally activate this for CUDA-enabled systems).
If you don't specify a CUDA build variant in a `packages.yaml` and you build your Kokkos-dependent project:
````
spack install superscience
````
you may end up just getting the default Kokkos (i.e. Serial).
Some exampls are included in the `yaml` folder for common platforms.

### Spack Environments
The encouraged method of using Spack is to use environments.
Rather than installing packages one-at-a-time, you add packages to an environment.
After adding all packages, you concretize and install them all.
Using environments, one can explicitly add a desired Kokkos for the environment, e.g.
````
spack add kokkos +cuda +cuda_lambda +volta70
````
All packages within the environment will build against the CUDA-enabled Kokkos,
even if they only request a default Kokkos.

## NVCC Wrapper
Kokkos is a C++ project, but often builds for the CUDA backend.
This is particularly problematic with CMake. At this point, `nvcc` does not accept all the flags that normally get passed to a C++ compiler.
Kokkos provides `nvcc_wrapper` that identifies correctly as a C++ compiler to CMake and accepts C++ flags, but uses `nvcc` as the underlying compiler.
`nvcc` itself also uses an underlying host compiler, e.g. GCC.

In Spack, the underlying host compiler is specified as below, e.g.:
````
spack install package %gcc@8.0.0
````
This is still valid for Kokkos. To use the special wrapper for CUDA builds, request a desired compiler and simply add the `+wrapper` variant.
````
spack install kokkos +cuda +wrapper %gcc@7.2.0
````
Downstream projects depending on Kokkos need to override their compiler.
Kokkos provides the compiler in a `kokkos_cxx` variable,
which points to either `nvcc_wrapper` when needed or the regular compiler otherwise.
Spack projects already do this to use MPI compiler wrappers.
````
def cmake_args(self):
  options = []
  ...
  options.append("-DCMAKE_CXX_COMPILER=%s" % self.spec["kokkos"].kokkos_cxx)
  ...
  return options
````
Note: `nvcc_wrapper` works with the MPI compiler wrappers.
If building your project with MPI, do NOT set your compiler to `nvcc_wrapper`.
Instead set your compiler to `mpicxx` and `nvcc_wrapper` will be used under the hood.
````
def cmake_args(self):
  options = []
  ...
  options.append("-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx)
  ...
  return options
````
To accomplish this, `nvcc_wrapper` must depend on MPI (even though it uses no MPI).
This has the unfortunate consequence that Kokkos CUDA projects not using MPI will implicitly depend on MPI anyway.
This behavior is necessary for now, but will hopefully be removed later.
When using environments, if MPI is not needed, you can remove the MPI dependency with:
````
spack add kokkos-nvcc-wrapper ~mpi
````


## Setting Up Kokkos Tutorials
Coming soon

## Kokkos Kernels (and other dependent projects)
Kokkos Kernels also defines a package that can be installed as, e.g.
````
spack install kokkos-kernels +serial +float
````
The main variants of Kokkos Kernels are the backend (e.g. serial, cuda, openmp), ETI types to be explicitly instantiated (e.g. float, double, complex_double), and third-party libraries (TPLs) used.
Kernels derives much of its configuration from the Kokkos installation itself (see above).
Thus Kokkos Kernels only has a few variants, in constrast to Kokkos which has dozens of variants.
For most options, tuning the configuration of Kokkos Kernels really means tuning the underlying Kokkos.


## Use with Testing
A Spack 'spec' provides a convenient way to define testing configurations for a CI infrastructure like Jenkins.
A spec such as:
````
kokkos-kernels@develop +float +double +cuda
````
defines a particular build of Kokkos Kernels that you want checked consistently on the develop branch.
By default, testing is not activated. To have Spack both build and test a given spec, run:
````
spack install --test=root kokkos-kernels
````
Here `--test=root` says to run tests on the 'root' package (not the dependent packages), which in this case is Kokkos Kernels.

##### [LICENSE](https://github.com/kokkos/kokkos/blob/master/LICENSE)

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

Under the terms of Contract DE-NA0003525 with NTESS,
the U.S. Government retains certain rights in this software.
