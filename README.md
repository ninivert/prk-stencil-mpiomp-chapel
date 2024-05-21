# prk-stencil-mpiomp-chapel

Compare a weak scaling for a star stencil computation.

We take
- Radius of the star stencil R = 2 (known at compile time)
- Grid size = base grid size * sqrt(number of nodes), such that amount of work per node stays constant. The base grid size is typically between `2**12` and `2**16`
- Number of iterations = 10000

**C+MPI+OMP version**

This repository includes a modified subset of files from: https://github.com/ParRes/Kernels.

`stencil.c` is modified such that it prints the detailed timing of communications and computations.

**Chapel version**

`stencil-opt.chpl` (and `stencil.chpl`) is adapted from https://github.com/chapel-lang/chapel/blob/main/test/studies/prk/Stencil/optimized/stencil-opt.chpl (respectively https://github.com/chapel-lang/chapel/blob/main/test/studies/prk/Stencil/stencil.chpl) to show details communication and computation times.

**Clusters**

Raw outputs are included in the `results/{daint,jed,marconi}` folder for a few clusters:
- CSCS Piz Daint: https://www.cscs.ch/computers/piz-daint
- EPFL Scitas Jed: https://scitas-doc.epfl.ch/supercomputers/jed
- Cineca Marconi: https://www.hpc.cineca.it/systems/hardware/marconi

Job files are generated (for every executable and every number of nodes from 1, 2, 4, ..., 256) for Slurm `sbatch` by using the `makejobs.py` jobs in `results`. In general,

```sh
# load the environment, this is cluster-specific
# <...>
# compile C+MPI++OMP version
pushd mpiopenmp/MPIOPENMP/Stencil
cd common && ln -s make.defs.nameOfTheCluster make.defs  # nameOfTheCluster in {cray,jed,marconi}
make -B stencil DEFAULT_OPT_FLAGS='-O3'
popd
# compile Chapel version(s)
pushd chapel
chpl --fast stencil-opt.chpl  # optimized version that uses stencilDist
chpl --fast -suseBlockDist=true -o stencil-blockdist stencil.chpl  # non-optimized blockDist version for comparison
popd
# make job files and submit some of them
pushd results
./makejobs.py
for f in job-{chpl-stencil-opt,mpiopenmp-stencil}-{0,1,2,3}; do sbatch $f; sleep 1; done;
```

## Cluster-specific instructions

### CSCS Piz Daint

Piz Daint is a Cray XC cluster, and Chapel automatically sets the correct environment when compiling. `CHPL_COMM=ugni`: https://chapel-lang.org/docs/main/platforms/cray.html.

```sh
module load daint-gpu craype-hugepages16M
module list
# 1) modules/3.2.11.4                                
# 2) craype-network-aries                            
# 3) cce/14.0.0                                      
# 4) craype/2.7.10                                   
# 5) cray-libsci/20.09.1                             
# 6) udreg/2.3.2-7.0.3.1_3.13__g5f0d670.ari          
# 7) ugni/6.0.14.0-7.0.3.1_6.2__g8101a58.ari         
# 8) pmi/5.0.17                                      
# 9) dmapp/7.1.1-7.0.3.1_3.17__g93a7e9f.ari          
# 10) gni-headers/5.0.12.0-7.0.3.1_3.7__gd0d73fe.ari  
# 11) xpmem/2.2.27-7.0.3.1_3.9__gada73ac.ari          
# 12) job/2.2.4-7.0.3.1_3.14__g36b56f4.ari            
# 13) dvs/2.12_2.2.224-7.0.3.1_3.12__gc77db2af
# 14) alps/6.6.67-7.0.3.1_3.18__gb91cd181.ari
# 15) rca/2.2.20-7.0.3.1_3.15__g8e3fb5b.ari
# 16) atp/3.14.5
# 17) perftools-base/21.09.0
# 18) PrgEnv-cray/6.0.10
# 19) cray-mpich/7.7.18
# 20) slurm/20.11.8-4
# 21) craype-haswell
# 22) cray-python/3.9.4.1
# 23) daint-gpu/21.09
# 24) craype-hugepages16M
# 25) Base-opts/2.4.142-7.0.3.1_3.7__g8f27585.ari

printchplenv --all
# machine info: Linux daint102 5.3.18-24.102-default #1 SMP Mon Jan 31 16:08:51 UTC 2022 (49453fa) x86_64
# CHPL_HOME: /users/nvadot/chapel/chapel *
# script location: /users/nvadot/chapel/chapel/util/chplenv
# CHPL_HOST_PLATFORM: cray-xc
# CHPL_HOST_COMPILER: gnu
#   CHPL_HOST_CC: gcc
#   CHPL_HOST_CXX: g++
# CHPL_HOST_ARCH: x86_64
# CHPL_TARGET_PLATFORM: cray-xc
# CHPL_TARGET_COMPILER: llvm
#   CHPL_TARGET_CC: /users/nvadot/chapel/chapel/third-party/llvm/install/cray-xc-x86_64/bin/clang
#   CHPL_TARGET_CXX: /users/nvadot/chapel/chapel/third-party/llvm/install/cray-xc-x86_64/bin/clang++
#   CHPL_TARGET_LD: /users/nvadot/chapel/chapel/third-party/llvm/install/cray-xc-x86_64/bin/clang++
# CHPL_TARGET_ARCH: x86_64
# CHPL_TARGET_CPU: haswell
# CHPL_LOCALE_MODEL: flat
# CHPL_COMM: ugni +
# CHPL_TASKS: qthreads
# CHPL_LAUNCHER: slurm-srun
# CHPL_TIMERS: generic
# CHPL_UNWIND: none
# CHPL_HOST_MEM: jemalloc
# CHPL_MEM: jemalloc
# CHPL_ATOMICS: cstdlib
#   CHPL_NETWORK_ATOMICS: ugni
# CHPL_GMP: bundled
# CHPL_HWLOC: bundled
# CHPL_RE2: bundled
# CHPL_LLVM: bundled +
#   CHPL_LLVM_SUPPORT: bundled
#   CHPL_LLVM_CONFIG: /users/nvadot/chapel/chapel/third-party/llvm/install/cray-xc-x86_64/bin/llvm-config
#   CHPL_LLVM_VERSION: 17
# CHPL_AUX_FILESYS: none
# CHPL_LIB_PIC: none
# CHPL_SANITIZE: none
# CHPL_SANITIZE_EXE: none

# in the case of 2**12 base grid size
# explicitly set --cpus-per-core to disable hyperthreading. On Piz Daint (XC50) Intel Xeon E5-2690 v3 has 12 cores, 2 threads per core
# constraint=gpu because I don't have access to the CPU-only partition. This is only a small test with walltimes <1min, so it's fine
./makejobs.py --partition=normal --constraint=gpu --base-gridsize=$(python -c 'print(2**12)') --cpus-per-task=12 --switches=1
```

### EPFL Scitas Jed

Jed runs on OpenUCX (`ompi_info` reports the configure command line `--with-ucx=/path/to/ucx-1.12.1-mcggqmcvjobtoc4p26hednzka6pjghgm`). I tried setting `CHPL_COMM_SUBTRATE=ucx` (see https://chapel-lang.org/docs/main/platforms/infiniband.html#ucx-alternative), but found the performance to be very poor, see `results/jed/substrate-ucx` (this is also expected, as `ucx` conduit is considered experimental).

An alternative is using the `mpi` substrate.


```sh
module load gcc openmpi

# to build the chapel runtime, we need to set MPI_CC, contained on Jed in the MPICC env var
cd $CHPL_HOME
./configure
MPI_CC=$MPICC make 

printchplenv --all
# machine info: Linux jed 5.14.0-70.30.1.el9_0.x86_64 #1 SMP PREEMPT Fri Oct 14 10:30:46 EDT 2022 x86_64
# CHPL_HOME: /home/vadot/chapel/chapel-2.0.1 *
# script location: /home/vadot/chapel/chapel-2.0.1/util/chplenv
# CHPL_HOST_PLATFORM: linux64
# CHPL_HOST_COMPILER: gnu
#   CHPL_HOST_CC: /ssoft/spack/syrah/v3/opt/spack/linux-rhel9-x86_64_v2/gcc-11.2.1/gcc-11.3.0-xt3pxujartqg46r6lercdmcya5bcxth4/bin/gcc
#   CHPL_HOST_CXX: /ssoft/spack/syrah/v3/opt/spack/linux-rhel9-x86_64_v2/gcc-11.2.1/gcc-11.3.0-xt3pxujartqg46r6lercdmcya5bcxth4/bin/g++
# CHPL_HOST_ARCH: x86_64
# CHPL_TARGET_PLATFORM: linux64
# CHPL_TARGET_COMPILER: llvm
#   CHPL_TARGET_CC: /home/vadot/chapel/chapel-2.0.1/third-party/llvm/install/linux64-x86_64/bin/clang --gcc-toolchain=/ssoft/spack/syrah/v3/opt/spack/linux-rhel9-x86_64_v2/gcc-11.2.1/gcc-11.3.0-xt3pxujartqg46r6lercdmcya5bcxth4
#   CHPL_TARGET_CXX: /home/vadot/chapel/chapel-2.0.1/third-party/llvm/install/linux64-x86_64/bin/clang++ --gcc-toolchain=/ssoft/spack/syrah/v3/opt/spack/linux-rhel9-x86_64_v2/gcc-11.2.1/gcc-11.3.0-xt3pxujartqg46r6lercdmcya5bcxth4
#   CHPL_TARGET_LD: mpicxx
# CHPL_TARGET_ARCH: x86_64
# CHPL_TARGET_CPU: native +
# CHPL_LOCALE_MODEL: flat
# CHPL_COMM: gasnet +
#   CHPL_COMM_SUBSTRATE: mpi +
#   CHPL_GASNET_SEGMENT: everything
#   CHPL_GASNET_VERSION: 1
# CHPL_TASKS: qthreads
# CHPL_LAUNCHER: slurm-srun +
# CHPL_TIMERS: generic
# CHPL_UNWIND: none
# CHPL_HOST_MEM: jemalloc
# CHPL_MEM: jemalloc +
# CHPL_ATOMICS: cstdlib
#   CHPL_NETWORK_ATOMICS: none
# CHPL_GMP: bundled
# CHPL_HWLOC: bundled
# CHPL_RE2: bundled
# CHPL_LLVM: bundled +
#   CHPL_LLVM_SUPPORT: bundled
#   CHPL_LLVM_CONFIG: /home/vadot/chapel/chapel-2.0.1/third-party/llvm/install/linux64-x86_64/bin/llvm-config
#   CHPL_LLVM_VERSION: 17
# CHPL_AUX_FILESYS: none
# CHPL_LIB_PIC: none
# CHPL_SANITIZE: none
# CHPL_SANITIZE_EXE: none

# make the jobfiles
cd /path/to/prk-stencil-mpiomp-chapel/results
./makejobs.py --qos-parallel=parallel --qos-serial=serial --cpus-per-task=72
```

### Cineca Marconi

This cluster has Intel OmniPath (100Gb/s) high-performance network (https://chapel-lang.org/docs/main/platforms/omnipath.html), so I set `CHPL_COMM_SUBSTRATE=ofi`.

We load the most recent version of gcc (that also has an available openmpi installation, for reasons that will become apparent later...) installed on the cluster:

```sh
module load gnu/7.3.0
```

Compiling `chpl` works, but the runtime fails to compile with a linker error:

```sh
make
# <...> stuff compiles
# <...> compiling the runtime
# /usr/bin/ld: .libs/assert.o: unrecognized relocation (0x2a) in section `.text'
# /usr/bin/ld: final link failed: Bad value
# clang: error: linker command failed with exit code 1 (use -v to see invocation)

which gcc
# /cineca/prod/opt/compilers/gnu/7.3.0/none/bin/gcc
gcc --version
# gcc (GCC) 7.3.0
# Copyright (C) 2017 Free Software Foundation, Inc.
# This is free software; see the source for copying conditions.  There is NO
# warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# NOTE : although gcc 7.4.0 is available on Marconi, openmpi 3.0.0 is only available with gnu 6.1.0 or 7.3.0
# (╯°□°）╯︵ ┻━┻ 

which ld
# /usr/bin/ld
ld --version
# GNU ld version 2.23.52.0.1-55.el7 20130226
# Copyright 2013 Free Software Foundation, Inc.
# This program is free software; you may redistribute it under the terms of
# the GNU General Public License version 3 or (at your option) a later version.
# This program has absolutely no warranty.

# !!! so old !!!
```

`ld` being from 11 years ago (at the time of writing) is the issue here. The solution is to use spack to load a newer version of binutils.


```sh
module load cmake/3.23.3 spack
# load a newever version of ld by loading binutils
# in retrospect, it might be possible to skip loading gcc@10 (although not sure with loading libfabric)
spack load gcc@10 binutils libfabric@1.14.1
# override the gcc compiler so that we can load openmpi for reasons explained below
module load gnu/7.3.0 openmpi/3.0.0--gnu--7.3.0 
# verify
which gcc
# /cineca/prod/opt/compilers/gnu/7.3.0/none/bin/gcc
which mpicc
# /cineca/prod/opt/compilers/openmpi/3.0.0/gnu--7.3.0/bin/mpicc
mpicc --showme
# gcc -I/cineca/prod/opt/compilers/openmpi/3.0.0/gnu--7.3.0/include -pthread -Wl,-rpath -Wl,/cineca/prod/opt/compilers/openmpi/3.0.0/gnu--7.3.0/lib -Wl,--enable-new-dtags -L/cineca/prod/opt/compilers/openmpi/3.0.0/gnu--7.3.0/lib -lmpi
gcc --version
# gcc (GCC) 7.3.0
# Copyright (C) 2017 Free Software Foundation, Inc.
# This is free software; see the source for copying conditions.  There is NO
# warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
which ld
# /marconi_work/PROJECTS/spack/preprod/02/install/0.18/linux-centos7-haswell/gcc-4.8.5/binutils-2.38-p6dl6v6xv4jv5dk4c4nbycruw5ji7m67/bin/ld
ld --version
# GNU ld (GNU Binutils) 2.38
# Copyright (C) 2022 Free Software Foundation, Inc.
# This program is free software; you may redistribute it under the terms of
# the GNU General Public License version 3 or (at your option) a later version.
# This program has absolutely no warranty.
```

Now the runtime build correctly !

By default Gasnet with ofi will try to use SSH for job launches, but in this case Marconi does not seem to allow ssh'ing into compute nodes:

```sh
salloc -N 1 --time=00:00:05 --partition=skl_fua_prod
# now in the salloc terminal
srun hostname
# r129c02s01
ssh r129c02s01
# ssh: connect to host r129c02s01 port 22: No route to host
# NOTE: although for some reason, it works with partition bdw_all_serial ??
```

So we have to set `GASNET_OFI_SPAWNER=mpi` and load `mpicc`.

```sh
printchplenv
# machine info: Linux r000u07l02 3.10.0-327.36.3.el7.x86_64 #1 SMP Mon Oct 24 16:09:20 UTC 2016 x86_64
# CHPL_HOME: /marconi/home/userexternal/nvadot00/chapel/chapel *
# script location: /marconi/home/userexternal/nvadot00/chapel/chapel/util/chplenv
# CHPL_HOST_PLATFORM: linux64
# CHPL_HOST_COMPILER: gnu
#   CHPL_HOST_CC: gcc
#   CHPL_HOST_CXX: g++
# CHPL_HOST_ARCH: x86_64
# CHPL_TARGET_PLATFORM: linux64
# CHPL_TARGET_COMPILER: llvm
#   CHPL_TARGET_CC: /marconi/home/userexternal/nvadot00/chapel/chapel/third-party/llvm/install/linux64-x86_64/bin/clang --gcc-toolchain=/cineca/prod/opt/compilers/gnu/7.3.0/none
#   CHPL_TARGET_CXX: /marconi/home/userexternal/nvadot00/chapel/chapel/third-party/llvm/install/linux64-x86_64/bin/clang++ --gcc-toolchain=/cineca/prod/opt/compilers/gnu/7.3.0/none
#   CHPL_TARGET_LD: /marconi/home/userexternal/nvadot00/chapel/chapel/third-party/llvm/install/linux64-x86_64/bin/clang++ --gcc-toolchain=/cineca/prod/opt/compilers/gnu/7.3.0/none
# CHPL_TARGET_ARCH: x86_64
# CHPL_TARGET_CPU: skylake +
# CHPL_LOCALE_MODEL: flat
# CHPL_COMM: gasnet +
#   CHPL_COMM_SUBSTRATE: ofi +
#   CHPL_GASNET_SEGMENT: everything
#   CHPL_GASNET_VERSION: 1
# CHPL_TASKS: qthreads
# CHPL_LAUNCHER: slurm-gasnetrun_ofi +
# CHPL_TIMERS: generic
# CHPL_UNWIND: none
# CHPL_HOST_MEM: jemalloc
# CHPL_MEM: jemalloc
# CHPL_ATOMICS: cstdlib
#   CHPL_NETWORK_ATOMICS: none
# CHPL_GMP: none
# CHPL_HWLOC: bundled
# CHPL_RE2: none
# CHPL_LLVM: bundled +
#   CHPL_LLVM_SUPPORT: bundled
#   CHPL_LLVM_CONFIG: /marconi/home/userexternal/nvadot00/chapel/chapel/third-party/llvm/install/linux64-x86_64/bin/llvm-config
#   CHPL_LLVM_VERSION: 17
# CHPL_AUX_FILESYS: none
# CHPL_LIB_PIC: none
# CHPL_SANITIZE: none
# CHPL_SANITIZE_EXE: none

# finally, to run the script it's good to have a pretty recent version of Python
module load python/3.9.4
./makejobs.py --partition=skl_fua_prod --cpus-per-task=48
```

## Results

**In general**

I observed on small grids (`--base-gridsize 2**8`) that Chapel has noticeable overhead. This overhead is less noticeable with larger grids (e.g. `2**12` used here). I also observed on single-locale tests that Chapel tends to perform better than OpenMP, which could explain that the `chpl-opt` curve lies above the `MPI+OMP` curve.

All curves scale linearly on the log-log plot. Efficiency shows that while Chapel is fast, there is a small overhead in the communications (that I expect to vanish relatively to larger problem sizes).

Cluster-specific plots follow. For Daint only a base gridsize of `2**12` is reported. Chapel unsurprisingly performs best on Daint, which is a Cray XC machine ; the Jed and Marconi clusters use `mpi` and `ofi` substrates respectively, and the overhead is larger, but still vanishes with larger grid sizes.

**Daint**

```sh
python3 results/plot.py -d results/daint/size12 --width=60 --height=16 --marker='-' | sed "s,\x1B\[[0-9;]*[a-zA-Z],,g"
```

```
size-12
                          Scaling test                      
    ┌──────────────────────────────────────────────────────┐
22.3┤ MM MPI+OMP                                          O│
    │ OO chpl-opt                                  O------M│
20.9┤                                        O-----M------ │
19.5┤                                 O------M-----        │
    │                              ---M------              │
18.1┤                           O-----                     │
    │                    O------                           │
16.7┤             O------                                  │
15.3┤       O-----M---                                     │
    │O------M-----                                         │
13.9┤M------                                               │
    └┬──────┬─────┬──────┬─────────────────────────────────┘
     0      1     2      3                                  
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O------O-----M------M------M-----M------M-----M------M│
    │        -----O------O                                 │
0.83┤                     ------O-----O------O-----O------O│
0.67┤                                                      │
    │                                                      │
0.50┤                                                      │
    │                                                      │
0.33┤                                                      │
0.17┤                                                      │
    │                                                      │
0.00┤                                                      │
    └┬──────┬─────┬──────┬─────────────────────────────────┘
     0      1     2      3                                  
Efficiency ~ t0/t    number of nodes [log2]                 
```

**Jed**

```sh
for d in results/jed/substrate-mpi/size-*; do basename $d; python3 results/plot.py -d $d --width=60 --height=16 --marker='-' | sed "s,\x1B\[[0-9;]*[a-zA-Z],,g"; done
```

```
size-11
                          Scaling test                      
    ┌──────────────────────────────────────────────────────┐
21.3┤ MM MPI+OMP                                          M│
    │ OO chpl-opt                    M---------M---------- │
20.0┤                     M----------                      │
18.8┤           M---------                                 │
    │M----------                                           │
17.6┤                                                      │
    │O                                         O----------O│
16.3┤ --                             O---------            │
15.1┤   ---                     -----                      │
    │      ---            O-----                           │
13.8┤         --O---------                                 │
    └┬──────────┬─────────┬──────────┬─────────────────────┘
     0          1         2          3                      
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O                                                     │
    │ ---                                                  │
0.83┤  - ----             M                                │
0.67┤   -    ---M--------- -----                           │
    │    -                      -----M                     │
0.50┤     --                          ---                  │
    │       -                            ---               │
0.33┤        -                              ---M           │
0.17┤         -                                 ----------M│
    │          -O                                          │
0.00┤            ---------O----------O---------O----------O│
    └┬──────────┬─────────┬──────────┬─────────────────────┘
     0          1         2          3                      
Efficiency ~ t0/t    number of nodes [log2]                 
size-12
                          Scaling test                      
    ┌──────────────────────────────────────────────────────┐
21.9┤ MM MPI+OMP                                          M│
    │ OO chpl-opt                                    ----- │
20.8┤                                          M-----      │
19.8┤                                M---------            │
    │                     M----------                      │
18.8┤           M---------                                O│
    │      -----                               O---------- │
17.7┤M-----                          O---------            │
16.7┤O                          -----                      │
    │ -----               O-----                           │
15.7┤      -----O---------                                 │
    └┬──────────┬─────────┬──────────┬─────────────────────┘
     0          1         2          3                      
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O                                                     │
    │ ----------M---------M                                │
0.83┤  -                   ----------M                     │
0.67┤   --                            -----                │
    │     -                                ----M----------M│
0.50┤      -                                               │
    │       --                                             │
0.33┤         -                                            │
0.17┤          -O---------O----------O---------O           │
    │                                           ----------O│
0.00┤                                                      │
    └┬──────────┬─────────┬──────────┬─────────────────────┘
     0          1         2          3                      
Efficiency ~ t0/t    number of nodes [log2]                 
size-13
                          Scaling test                      
     ┌─────────────────────────────────────────────────────┐
21.54┤ MM MPI+OMP                                         M│
     │ OO chpl-opt                              M--------- │
20.73┤                                     -----          O│
19.92┤                               M-----          ----- │
     │                          -----           O----      │
19.12┤                     M----     O----------           │
     │                -----       ---                      │
18.31┤          M-----         ---                         │
17.50┤     -----           O---                            │
     │M----     O----------                                │
16.70┤O---------                                           │
     └┬─────────┬──────────┬─────────┬─────────────────────┘
      0         1          2         3                      
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O----------M                                          │
    │ ---        ---------M----------M---------M           │
0.83┤    ----                                   -----      │
0.67┤        ---O                                    -----M│
    │            -----               O                     │
0.50┤                 ----O---------- ---------O----------O│
    │                                                      │
0.33┤                                                      │
0.17┤                                                      │
    │                                                      │
0.00┤                                                      │
    └┬──────────┬─────────┬──────────┬─────────────────────┘
     0          1         2          3                      
Efficiency ~ t0/t    number of nodes [log2]                 
size-14
                          Scaling test                      
     ┌─────────────────────────────────────────────────────┐
20.76┤ MM MPI+OMP                                         O│
     │ OO chpl-opt                                   ----- │
20.12┤                                          O----      │
19.47┤                               O----------           │
     │                          -----                      │
18.83┤                     M------                         │
     │                -----O---                            │
18.18┤          M----------                                │
17.54┤       ---O-----                                     │
     │    ------                                           │
16.89┤O----                                                │
     └┬─────────┬──────────┬─────────┬─────────────────────┘
      0         1          2         3                      
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O----------M---------M                                │
    │ ----------O          -----                           │
0.83┤            -----          -----M                     │
0.67┤                 ----O----------O---                  │
    │                                 ---------O           │
0.50┤                                       ---M-----      │
    │                                           ----------O│
0.33┤                                                      │
0.17┤                                                      │
    │                                                      │
0.00┤                                                      │
    └┬──────────┬─────────┬──────────┬─────────────────────┘
     0          1         2          3                      
Efficiency ~ t0/t    number of nodes [log2]                 
size-15
                          Scaling test                      
     ┌─────────────────────────────────────────────────────┐
21.51┤ MM MPI+OMP                                         O│
     │ OO chpl-opt                                   ----- │
20.74┤                                          O----     M│
19.97┤                                     -----M--------- │
     │                               O----------           │
19.20┤                          -----                      │
     │                     O----                           │
18.43┤                -----                                │
17.65┤          O-----                                     │
     │     -----                                           │
16.88┤O----                                                │
     └┬─────────┬──────────┬─────────┬─────────────────────┘
      0         1          2         3                      
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O                                                     │
    │ ----------O---------O----------O                     │
0.83┤                      -----      ---------O----------O│
0.67┤                           -----M                     │
    │                                 ---------M           │
0.50┤                                           -----      │
    │                                                -----M│
0.33┤                                                      │
0.17┤                                                      │
    │                                                      │
0.00┤                                                      │
    └┬──────────┬─────────┬──────────┬─────────────────────┘
     0          1         2          3                      
Efficiency ~ t0/t    number of nodes [log2]                 
```

**Marconi**

```sh
for d in results/marconi/size*; do basename $d; python3 results/plot.py -d $d --width=60 --height=16 --marker='-' | sed "s,\x1B\[[0-9;]*[a-zA-Z],,g"; done
```

```
size12
                          Scaling test                      
     ┌─────────────────────────────────────────────────────┐
16.39┤ MM MPI+OMP                                         M│
     │ OO chpl-opt                                     --- │
15.86┤O                                             ---    │
15.33┤ --                                       ----       │
     │   --                                  ---           │
14.80┤M    --                            M---              │
     │ ----  --                      ----                 O│
14.27┤     ------               -----                ----- │
13.74┤         ----         ----               ------      │
     │             ----M----             O-----            │
13.21┤               --O-----------------                  │
     └┬────────────────┬─────────────────┬────────────────┬┘
      0                1                 2                3 
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O                                                     │
    │ --                                                   │
0.83┤   --                                                 │
0.67┤     --                                               │
    │       ---                                            │
0.50┤         ---                                          │
    │           ---                                       M│
0.33┤             ---                   M----------------- │
0.17┤               ---M----------------                   │
    │                 -O----------------O                  │
0.00┤                                    -----------------O│
    └┬─────────────────┬────────────────┬─────────────────┬┘
     0                 1                2                 3 
Efficiency ~ t0/t    number of nodes [log2]                 
size13
                          Scaling test                      
     ┌─────────────────────────────────────────────────────┐
18.58┤ MM MPI+OMP                                         M│
     │ OO chpl-opt                                   ----- │
17.99┤                                         ------      │
17.40┤                                   M-----            │
     │                          ---------                  │
16.81┤                 M--------                           │
     │M----------------                                   O│
16.21┤O                                           -------- │
15.62┤ -----                             O--------         │
     │      ------              ---------                  │
15.03┤            -----O--------                           │
     └┬────────────────┬─────────────────┬────────────────┬┘
      0                1                 2                3 
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O                                                     │
    │ ----                                                 │
0.83┤   -------                                            │
0.67┤     --   ----                                        │
    │       ---    ----M                                  M│
0.50┤          --       ----------------M----------------- │
    │            --                                        │
0.33┤              --                                      │
0.17┤                --O----------------O-----------------O│
    │                                                      │
0.00┤                                                      │
    └┬─────────────────┬────────────────┬─────────────────┬┘
     0                 1                2                 3 
Efficiency ~ t0/t    number of nodes [log2]                 
size14
                          Scaling test                      
     ┌─────────────────────────────────────────────────────┐
18.67┤ MM MPI+OMP                                         M│
     │ OO chpl-opt                                    ---- │
18.26┤                                            ----     │
17.84┤                                        ----        O│
     │                                   M----       ----- │
17.43┤                          ---------      ------      │
     │                 M--------         O-----            │
17.01┤            -----            ------                  │
16.59┤      ------           ------                        │
     │M-----           O-----                              │
16.18┤O----------------                                    │
     └┬────────────────┬─────────────────┬────────────────┬┘
      0                1                 2                3 
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O                                                     │
    │ -----------------M                                   │
0.83┤     -----         --------                           │
0.67┤          ----             --------M                  │
    │              ----O                 -----------------M│
0.50┤                   ----------------O                  │
    │                                    -----------------O│
0.33┤                                                      │
0.17┤                                                      │
    │                                                      │
0.00┤                                                      │
    └┬─────────────────┬────────────────┬─────────────────┬┘
     0                 1                2                 3 
Efficiency ~ t0/t    number of nodes [log2]                 
size15
                          Scaling test                      
     ┌─────────────────────────────────────────────────────┐
18.79┤ MM MPI+OMP                                         M│
     │ OO chpl-opt                                    ---- │
18.36┤                                            ----     │
17.93┤                                        ----        O│
     │                                   M----       ----- │
17.49┤                          ---------      ------      │
     │                 M--------         O-----            │
17.06┤            -----            ------                  │
16.63┤      ------           ------                        │
     │M-----           O-----                              │
16.19┤O----------------                                    │
     └┬────────────────┬─────────────────┬────────────────┬┘
      0                1                 2                3 
MFlops/s [log2]      number of nodes [log2]                 
                           Efficiency                       
    ┌──────────────────────────────────────────────────────┐
1.00┤O                                                     │
    │ -----------------M                                   │
0.83┤     -----         --------                           │
0.67┤          ----             --------M-----------------M│
    │              ----O                                   │
0.50┤                   ----------------O                  │
    │                                    -----------------O│
0.33┤                                                      │
0.17┤                                                      │
    │                                                      │
0.00┤                                                      │
    └┬─────────────────┬────────────────┬─────────────────┬┘
     0                 1                2                 3 
Efficiency ~ t0/t    number of nodes [log2]                 
```
