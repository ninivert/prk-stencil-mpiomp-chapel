#!/usr/bin/python3

import math, os, stat, argparse
from pathlib import Path

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-a', '--account', type=str, help='--account for slurm job', required=True)
parser.add_argument('--iterations', type=int, default=100, help='number of iterations')
parser.add_argument('--base-gridsize', type=int, default=2**16, help='grid size when running on one node')
parser.add_argument('--walltime', type=str, default='00:00:01', help='--time for slurm job')
parser.add_argument('--partition', type=str, default='normal', help='--partition for slurm job')
parser.add_argument('--constraint', type=str, default='gpu', help='--constraint for slurm job')
args = parser.parse_args()

from pprint import pprint
pprint(args)

jobheader = """\
#!/bin/bash -l
#SBATCH --job-name="{LANG}-{EXE}-{LOGNUMNODES}"
#SBATCH --account="{ACCOUNT}"
#SBATCH --time={WALLTIME}
#SBATCH --nodes={NUMNODES}
#SBATCH --partition={PARTITION}
#SBATCH --constraint={CONSTRAINT}
#SBATCH --output=result-{LANG}-{EXE}-{LOGNUMNODES}.out
## https://user.cscs.ch/access/running/#electrical-groups
#SBATCH --switches=1
"""

jobcode = {}

jobcode["mpiopenmp"] = """\
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=1
## disable hyperthreading. On Piz Daint (XC50) Intel Xeon E5-2690 v3 has 12 cores, 2 threads per core
#SBATCH --cpus-per-task=12

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

echo ">>> module list"
module list

echo ">>> srun log"
srun --exclusive ../mpiomp/MPIOPENMP/Stencil/{EXE} $OMP_NUM_THREADS {NUMITER} {GRIDSIZE}
"""

jobcode["chpl"] = """\
# we don't set --cpus-per-task or --ntasks variables, we let the Chapel launcher figure it out
# (and the program prints out numLocales and maxTaskPar)

echo ">>> printchplenv --all"
$CHPL_HOME/util/printchplenv --all

echo ">>> module list"
module list

echo ">>> compilation info"
../chapel/{EXE} --about

echo ">>> srun log"
../chapel/{EXE} -nl {NUMNODES} --iterations {NUMITER} --order {GRIDSIZE}
"""

for lang, exe in ("chpl", "stencil-opt"), ("chpl", "stencil-blockdist"), ("chpl", "stencil-stencildist"), ("chpl", "stencil-opt-v1.22"), ("mpiopenmp", "stencil"):
    for lognumnodes in range(0, 9):
        numnodes = 2**lognumnodes
        gridsize = int(args.base_gridsize * math.sqrt(numnodes))
        jobscript = (jobheader + jobcode[lang]).format(
            LOGNUMNODES=lognumnodes, NUMNODES=numnodes, GRIDSIZE=gridsize, NUMITER=args.iterations,
            LANG=lang, EXE=exe, ACCOUNT=args.account, WALLTIME=args.walltime, PARTITION=args.partition, CONSTRAINT=args.constraint
        )
        fp = Path(f"job-{lang}-{exe}-{lognumnodes}")
        with open(fp, 'w') as f:
            f.write(jobscript)
        fp.chmod(fp.stat().st_mode | stat.S_IEXEC)
