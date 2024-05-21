#!/usr/bin/python3

import math, os, stat, argparse
from pathlib import Path

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--account', type=str, default=None, help='--account for slurm job. leave empty for default account')
parser.add_argument('--iterations', type=int, default=100, help='number of iterations')
parser.add_argument('--base-gridsize', type=int, default=2**16, help='grid size when running on one node')
parser.add_argument('--walltime', type=str, default='00:00:01', help='--time for slurm job')
parser.add_argument('--partition', type=str, default=None, help='--partition for slurm job. leave empty for default partition')
parser.add_argument('--constraint', type=str, default=None, help='--constraint for slurm job. leave empty for default constraint')
parser.add_argument('--qos-serial', type=str, default=None, help='--qos when num nodes == 1. leave empty for default qos')
parser.add_argument('--qos-parallel', type=str, default=None, help='--qos when num nodes > 1. leave empty for default qos')
parser.add_argument('--cpus-per-task', type=str, default=None, help='--cpus-per-task for slurm job. leave empty for default')
parser.add_argument('--switches', type=str, default=None, help='--switches set to 1 to stay within the same electrical group')
args = parser.parse_args()

from pprint import pprint
pprint(args)

jobheader = """\
#!/bin/bash -l
#SBATCH --job-name="{LANG}-{EXE}-{LOGNUMNODES}"
#SBATCH --output="result-{LANG}-{EXE}-{LOGNUMNODES}.out"
{SBATCH_ACCOUNT}
{SBATCH_WALLTIME}
{SBATCH_NUMNODES}
#SBATCH --exclusive
#SBATCH --mem=0
{SBATCH_PARTITION}
{SBATCH_CONSTRAINT}
{SBATCH_SWITCHES}
{SBATCH_CPUSPERTASK}
"""

jobcode = {}

jobcode["mpiopenmp"] = """\
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=1

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

for lang, exe in ("chpl", "stencil-opt"), ("chpl", "stencil-blockdist"), ("chpl", "stencil-stencildist"), ("mpiopenmp", "stencil"):
    for lognumnodes in range(0, 9):
        numnodes = 2**lognumnodes
        gridsize = int(args.base_gridsize * math.sqrt(numnodes))
        jobscript = (jobheader + jobcode[lang]).format(
            NUMNODES=numnodes, LOGNUMNODES=lognumnodes, GRIDSIZE=gridsize, NUMITER=args.iterations,
            LANG=lang, EXE=exe,\
            SBATCH_ACCOUNT='' if args.account is None else f'#SBATCH --account="{args.account}"', 
            SBATCH_WALLTIME='' if args.walltime is None else f'#SBATCH --time="{args.walltime}"',
            SBATCH_NUMNODES=f'#SBATCH --nodes={numnodes}',
            SBATCH_PARTITION='' if args.partition is None else f'#SBATCH --partition="{args.partition}"',
            SBATCH_CONSTRAINT='' if args.constraint is None else f'#SBATCH --constraint={args.constraint}',
            SBATCH_SWITCHES='' if args.switches is None else f'#SBATCH --switches={args.switches}',
            SBATCH_CPUSPERTASK='' if args.cpus_per_task is None else f'#SBATCH --cpus-per-task={args.cpus_per_task}',
            SBATCH_QOS=('' if args.qos_serial is None else f'#SBATCH --qos={args.qos_serial}') if numnodes == 1 else \
                       ('' if args.qos_parallel is None else f'#SBATCH --qos={args.qos_parallel}')
        )
        fp = Path(f"job-{lang}-{exe}-{lognumnodes}")
        with open(fp, 'w') as f:
            f.write(jobscript)
        fp.chmod(fp.stat().st_mode | stat.S_IEXEC)
