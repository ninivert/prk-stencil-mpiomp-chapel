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

MFlops/s (we expect number of nodes ~ MFlops ~ 1/walltime):

```sh
cd results && grep 'MFlops/s' result-*.out
# result-chpl-stencil-blockdist-0.out:Rate (MFlops/s): 5718.770795  Avg time (s): 0.000210985  
# result-chpl-stencil-blockdist-1.out:Rate (MFlops/s): 6373.674810  Avg time (s): 0.000382058  
# result-chpl-stencil-blockdist-2.out:Rate (MFlops/s): 11568.376759  Avg time (s): 0.000423846 
# result-chpl-stencil-blockdist-3.out:Rate (MFlops/s): 19732.235709  Avg time (s): 0.000499163  
# result-chpl-stencil-blockdist-4.out:Rate (MFlops/s): 35904.429223  Avg time (s): 0.000550562  
# result-chpl-stencil-blockdist-5.out:Rate (MFlops/s): 64904.373252  Avg time (s): 0.000610399  
# result-chpl-stencil-blockdist-6.out:Rate (MFlops/s): 109502.789410  Avg time (s): 0.00072492  
# result-chpl-stencil-blockdist-7.out:Rate (MFlops/s): 177335.739180  Avg time (s): 0.000896095
# result-chpl-stencil-blockdist-8.out:Rate (MFlops/s): 363065.576429  Avg time (s): 0.000876274 
# result-chpl-stencil-opt-0.out:Rate (MFlops/s): 51729.761711  Avg time (s): 2.33246e-05                  
# result-chpl-stencil-opt-1.out:Rate (MFlops/s): 15504.278913  Avg time (s): 0.000157061                   
# result-chpl-stencil-opt-2.out:Rate (MFlops/s): 17933.643687  Avg time (s): 0.000273409                   
# result-chpl-stencil-opt-3.out:Rate (MFlops/s): 33231.901627  Avg time (s): 0.00029639                    
# result-chpl-stencil-opt-4.out:Rate (MFlops/s): 49095.887689  Avg time (s): 0.000402632                    
# result-chpl-stencil-opt-5.out:Rate (MFlops/s): 87528.937457  Avg time (s): 0.000452623
# result-chpl-stencil-opt-6.out:Rate (MFlops/s): 100693.410241  Avg time (s): 0.000788341
# result-chpl-stencil-opt-7.out:Rate (MFlops/s): 249677.655642  Avg time (s): 0.000636459
# result-chpl-stencil-opt-8.out:Rate (MFlops/s): 275685.284717  Avg time (s): 0.00115401
# result-chpl-stencil-stencildist-0.out:Rate (MFlops/s): 4926.889403  Avg time (s): 0.000244896
# result-chpl-stencil-stencildist-1.out:Rate (MFlops/s): 6387.207937  Avg time (s): 0.000381249
# result-chpl-stencil-stencildist-2.out:Rate (MFlops/s): 9774.551323  Avg time (s): 0.000501631
# result-chpl-stencil-stencildist-3.out:Rate (MFlops/s): 15918.187858  Avg time (s): 0.000618764
# result-chpl-stencil-stencildist-4.out:Rate (MFlops/s): 25185.133845  Avg time (s): 0.000784892
# result-chpl-stencil-stencildist-5.out:Rate (MFlops/s): 43283.345777  Avg time (s): 0.000915308
# result-chpl-stencil-stencildist-6.out:Rate (MFlops/s): 87557.971839  Avg time (s): 0.000906608
# result-chpl-stencil-stencildist-7.out:Rate (MFlops/s): 103107.417607  Avg time (s): 0.0015412
# result-chpl-stencil-stencildist-8.out:Rate (MFlops/s): 192475.513195  Avg time (s): 0.00165291
# result-mpiopenmp-stencil-0.out:Rate (MFlops/s), including communication and increment time: 9307.714335 
# result-mpiopenmp-stencil-1.out:Rate (MFlops/s), including communication and increment time: 18071.849676 
# result-mpiopenmp-stencil-2.out:Rate (MFlops/s), including communication and increment time: 32747.665417 
# result-mpiopenmp-stencil-3.out:Rate (MFlops/s), including communication and increment time: 65651.559075 
# result-mpiopenmp-stencil-4.out:Rate (MFlops/s), including communication and increment time: 123187.112312 
# result-mpiopenmp-stencil-5.out:Rate (MFlops/s), including communication and increment time: 251367.062402 
# result-mpiopenmp-stencil-6.out:Rate (MFlops/s), including communication and increment time: 469215.976793 
# result-mpiopenmp-stencil-7.out:Rate (MFlops/s), including communication and increment time: 901721.422619 
# result-mpiopenmp-stencil-8.out:Rate (MFlops/s), including communication and increment time: 1314397.692118
```

communication times (note: for blockdist, the communications happen during the stencil, so these times are not representative):

```sh
grep -i 'comm time' result-*.out
# result-chpl-stencil-blockdist-0.out:comm time =      total 0.000253, avg 2.53e-08
# result-chpl-stencil-blockdist-1.out:comm time =      total 0.000252, avg 2.52e-08
# result-chpl-stencil-blockdist-2.out:comm time =      total 0.000245, avg 2.45e-08
# result-chpl-stencil-blockdist-3.out:comm time =      total 0.000248, avg 2.48e-08
# result-chpl-stencil-blockdist-4.out:comm time =      total 0.000263, avg 2.63e-08
# result-chpl-stencil-blockdist-5.out:comm time =      total 0.000238, avg 2.38e-08
# result-chpl-stencil-blockdist-6.out:comm time =      total 0.000253, avg 2.53e-08
# result-chpl-stencil-blockdist-7.out:comm time =      total 0.000283, avg 2.83e-08
# result-chpl-stencil-blockdist-8.out:comm time =      total 0.000294, avg 2.94e-08
# result-chpl-stencil-opt-0.out:comm time =      total 0.037894, avg 3.7894e-06
# result-chpl-stencil-opt-1.out:comm time =      total 1.14631, avg 0.000114631
# result-chpl-stencil-opt-2.out:comm time =      total 2.27818, avg 0.000227818
# result-chpl-stencil-opt-3.out:comm time =      total 2.45184, avg 0.000245184
# result-chpl-stencil-opt-4.out:comm time =      total 3.43848, avg 0.000343848
# result-chpl-stencil-opt-5.out:comm time =      total 3.71855, avg 0.000371855
# result-chpl-stencil-opt-6.out:comm time =      total 6.20309, avg 0.000620309
# result-chpl-stencil-opt-7.out:comm time =      total 4.58092, avg 0.000458092
# result-chpl-stencil-opt-8.out:comm time =      total 8.21222, avg 0.000821222
# result-chpl-stencil-stencildist-0.out:comm time =      total 0.038626, avg 3.8626e-06
# result-chpl-stencil-stencildist-1.out:comm time =      total 1.16877, avg 0.000116877
# result-chpl-stencil-stencildist-2.out:comm time =      total 2.25004, avg 0.000225004
# result-chpl-stencil-stencildist-3.out:comm time =      total 2.3541, avg 0.00023541
# result-chpl-stencil-stencildist-4.out:comm time =      total 3.45764, avg 0.000345764
# result-chpl-stencil-stencildist-5.out:comm time =      total 3.60483, avg 0.000360483
# result-chpl-stencil-stencildist-6.out:comm time =      total 3.75326, avg 0.000375326
# result-chpl-stencil-stencildist-7.out:comm time =      total 6.89182, avg 0.000689182
# result-chpl-stencil-stencildist-8.out:comm time =      total 8.50537, avg 0.000850537
# result-mpiopenmp-stencil-0.out:Comm time [s] (max of all ranks):      total 0.000529, avg 0.000000
# result-mpiopenmp-stencil-1.out:Comm time [s] (max of all ranks):      total 0.074500, avg 0.000007
# result-mpiopenmp-stencil-2.out:Comm time [s] (max of all ranks):      total 0.145751, avg 0.000015
# result-mpiopenmp-stencil-3.out:Comm time [s] (max of all ranks):      total 0.219346, avg 0.000022
# result-mpiopenmp-stencil-4.out:Comm time [s] (max of all ranks):      total 0.252071, avg 0.000025
# result-mpiopenmp-stencil-5.out:Comm time [s] (max of all ranks):      total 0.295243, avg 0.000030
# result-mpiopenmp-stencil-6.out:Comm time [s] (max of all ranks):      total 0.334908, avg 0.000033
# result-mpiopenmp-stencil-7.out:Comm time [s] (max of all ranks):      total 0.473501, avg 0.000047
# result-mpiopenmp-stencil-8.out:Comm time [s] (max of all ranks):      total 1.062291, avg 0.000106
```

stencil times (we expect constant stencil times for a strong scaling):

```sh
grep -i 'stencil time' result-*.out
# result-chpl-stencil-blockdist-0.out:stencil time =   total 2.03937, avg 0.000203937
# result-chpl-stencil-blockdist-1.out:stencil time =   total 3.63914, avg 0.000363914
# result-chpl-stencil-blockdist-2.out:stencil time =   total 4.03689, avg 0.000403689
# result-chpl-stencil-blockdist-3.out:stencil time =   total 4.76875, avg 0.000476875
# result-chpl-stencil-blockdist-4.out:stencil time =   total 5.23005, avg 0.000523005
# result-chpl-stencil-blockdist-5.out:stencil time =   total 5.71985, avg 0.000571985
# result-chpl-stencil-blockdist-6.out:stencil time =   total 6.52925, avg 0.000652925
# result-chpl-stencil-blockdist-7.out:stencil time =   total 7.84955, avg 0.000784955
# result-chpl-stencil-blockdist-8.out:stencil time =   total 7.12846, avg 0.000712846
# result-chpl-stencil-opt-0.out:stencil time =   total 0.121197, avg 1.21197e-05
# result-chpl-stencil-opt-1.out:stencil time =   total 0.251713, avg 2.51713e-05
# result-chpl-stencil-opt-2.out:stencil time =   total 0.262312, avg 2.62312e-05
# result-chpl-stencil-opt-3.out:stencil time =   total 0.294854, avg 2.94854e-05
# result-chpl-stencil-opt-4.out:stencil time =   total 0.335984, avg 3.35984e-05
# result-chpl-stencil-opt-5.out:stencil time =   total 0.464263, avg 4.64263e-05
# result-chpl-stencil-opt-6.out:stencil time =   total 0.934809, avg 9.34809e-05
# result-chpl-stencil-opt-7.out:stencil time =   total 0.947272, avg 9.47272e-05
# result-chpl-stencil-opt-8.out:stencil time =   total 1.76124, avg 0.000176124
# result-chpl-stencil-stencildist-0.out:stencil time =   total 2.33527, avg 0.000233527
# result-chpl-stencil-stencildist-1.out:stencil time =   total 2.46613, avg 0.000246613
# result-chpl-stencil-stencildist-2.out:stencil time =   total 2.56828, avg 0.000256828
# result-chpl-stencil-stencildist-3.out:stencil time =   total 3.61208, avg 0.000361208
# result-chpl-stencil-stencildist-4.out:stencil time =   total 4.11926, avg 0.000411926
# result-chpl-stencil-stencildist-5.out:stencil time =   total 5.19918, avg 0.000519918
# result-chpl-stencil-stencildist-6.out:stencil time =   total 4.81045, avg 0.000481045
# result-chpl-stencil-stencildist-7.out:stencil time =   total 7.27298, avg 0.000727298
# result-chpl-stencil-stencildist-8.out:stencil time =   total 6.26581, avg 0.000626581
# result-mpiopenmp-stencil-0.out:Stencil time [s] (max of all ranks):   total 1.025441, avg 0.000103
# result-mpiopenmp-stencil-1.out:Stencil time [s] (max of all ranks):   total 0.998884, avg 0.000100
# result-mpiopenmp-stencil-2.out:Stencil time [s] (max of all ranks):   total 1.086116, avg 0.000109
# result-mpiopenmp-stencil-3.out:Stencil time [s] (max of all ranks):   total 1.052474, avg 0.000105
# result-mpiopenmp-stencil-4.out:Stencil time [s] (max of all ranks):   total 1.094922, avg 0.000109
# result-mpiopenmp-stencil-5.out:Stencil time [s] (max of all ranks):   total 1.060298, avg 0.000106
# result-mpiopenmp-stencil-6.out:Stencil time [s] (max of all ranks):   total 1.100519, avg 0.000110
# result-mpiopenmp-stencil-7.out:Stencil time [s] (max of all ranks):   total 1.067917, avg 0.000107
# result-mpiopenmp-stencil-8.out:Stencil time [s] (max of all ranks):   total 1.108560, avg 0.000111
```
