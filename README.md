# prk-stencil-mpiomp-chapel

Compare a strong scaling for a star stencil computation.

We take
- Radius of the star stencil R = 2 (known at compile time)
- Grid size = 256 * sqrt(number of nodes)
- Number of iterations = 10000

`results` includes the timings from running on Piz Daint (https://www.cscs.ch/computers/piz-daint).

## Compilation

### Environment

We load `daint-gpu`, `craype-hugepages16M`.
`Base-opts` gets loaded automatically when submitting via `sbatch`.

output of `module list`:

```
1) modules/3.2.11.4                                
2) craype-network-aries                            
3) cce/14.0.0                                      
4) craype/2.7.10                                   
5) cray-libsci/20.09.1                             
6) udreg/2.3.2-7.0.3.1_3.13__g5f0d670.ari          
7) ugni/6.0.14.0-7.0.3.1_6.2__g8101a58.ari         
8) pmi/5.0.17                                      
9) dmapp/7.1.1-7.0.3.1_3.17__g93a7e9f.ari          
10) gni-headers/5.0.12.0-7.0.3.1_3.7__gd0d73fe.ari  
11) xpmem/2.2.27-7.0.3.1_3.9__gada73ac.ari          
12) job/2.2.4-7.0.3.1_3.14__g36b56f4.ari            
13) dvs/2.12_2.2.224-7.0.3.1_3.12__gc77db2af
14) alps/6.6.67-7.0.3.1_3.18__gb91cd181.ari
15) rca/2.2.20-7.0.3.1_3.15__g8e3fb5b.ari
16) atp/3.14.5
17) perftools-base/21.09.0
18) PrgEnv-cray/6.0.10
19) cray-mpich/7.7.18
20) slurm/20.11.8-4
21) craype-haswell
22) cray-python/3.9.4.1
23) daint-gpu/21.09
24) craype-hugepages16M
25) Base-opts/2.4.142-7.0.3.1_3.7__g8f27585.ari
```

### MPI+OpenMP version

This repository includes a modified subset of files from: https://github.com/ParRes/Kernels.

`stencil.c` is modified such that it prints the detailed timing of communications and computations.

To compile:

```sh
cd mpiopenmp/MPIOPENMP/Stencil
# on Piz Daint, there is a bug that crashes the compiler with the cce/12.0.3, so use a newer version
# module switch cce/12.0.3 cce/14.0.0
make -B stencil DEFAULT_OPT_FLAGS='-O3'
```

### Chapel version

`stencil-opt.chpl` (and `stencil.chpl`) is adapted from https://github.com/chapel-lang/chapel/blob/main/test/studies/prk/Stencil/optimized/stencil-opt.chpl (respectively https://github.com/chapel-lang/chapel/blob/main/test/studies/prk/Stencil/stencil.chpl) to show details communication and computation times.

```sh
cd chapel
chpl --fast stencil-opt.chpl
chpl --fast -suseBlockDist=true -o stencil-blockdist stencil.chpl
chpl --fast -suseStencilDist=true -o stencil-stencildist stencil.chpl
```

## Submitting jobs

We generate a jobscript for every executable and every number of nodes from 1, 2, 4, ..., 256.

```sh
cd results
./makejobs.py -a youraccount
# creates:
#   job-chpl-stencil-blockdist-0
#   job-chpl-stencil-blockdist-1
#   job-chpl-stencil-blockdist-2
#   job-chpl-stencil-blockdist-3
#   job-chpl-stencil-blockdist-4
#   job-chpl-stencil-blockdist-5
#   job-chpl-stencil-blockdist-6
#   job-chpl-stencil-blockdist-7
#   job-chpl-stencil-blockdist-8
#   job-chpl-stencil-opt-0
#   job-chpl-stencil-opt-1
#   job-chpl-stencil-opt-2
#   job-chpl-stencil-opt-3
#   job-chpl-stencil-opt-4
#   job-chpl-stencil-opt-5
#   job-chpl-stencil-opt-6
#   job-chpl-stencil-opt-7
#   job-chpl-stencil-opt-8
#   job-chpl-stencil-stencildist-0
#   job-chpl-stencil-stencildist-1
#   job-chpl-stencil-stencildist-2
#   job-chpl-stencil-stencildist-3
#   job-chpl-stencil-stencildist-4
#   job-chpl-stencil-stencildist-5
#   job-chpl-stencil-stencildist-6
#   job-chpl-stencil-stencildist-7
#   job-chpl-stencil-stencildist-8
#   job-mpiopenmp-stencil-0
#   job-mpiopenmp-stencil-1
#   job-mpiopenmp-stencil-2
#   job-mpiopenmp-stencil-3
#   job-mpiopenmp-stencil-4
#   job-mpiopenmp-stencil-5
#   job-mpiopenmp-stencil-6
#   job-mpiopenmp-stencil-7
#   job-mpiopenmp-stencil-8
```

Submit the jobs manually, e.g. using a batch for loop:

```sh
for job in job-chpl-stencil-opt-{0,1,2}; do sbatch $job; sleep 1; done;
```

## Parsing results

TODO
