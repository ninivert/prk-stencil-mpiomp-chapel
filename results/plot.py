import glob
import re
import os
import math
from pprint import pprint
from pathlib import Path
import argparse
import numpy as np
import plotext as plt

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', type=Path, default=Path('.'), help='directory containing the .out files')
parser.add_argument('--width', type=float, default=60, help='width of the plot')
parser.add_argument('--height', type=float, default=15, help='height of the plot')
parser.add_argument('--marker', type=str, default='braille', help='marker to use for the lines')
parser.add_argument('--theme', type=str, default='pro', help='plot theme')
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()

# this is the worst script ive even written, a result of late night coding lmao

dat = {}

for name, reflops, rewalltime, globpat in (
    ('MPI+OMP', r'(?:MFlops\/s.* )([\d\.]+)', r'(?:.*total )([\d\.]+)', str(args.directory / 'result-mpiopenmp-stencil-*.out')),
    ('chpl-opt', r'(?:MFlops\/s\): )([\d\.]+)', r'(?:.*total )([\d\.]+)', str(args.directory / 'result-chpl-stencil-opt-*.out')),
    # ('chpl-stencildist', r'(?:MFlops\/s\): )([\d\.]+)', 'result-chpl-stencil-stencildist-*.out'),
    # ('chpl-blockdist', r'(?:MFlops\/s\): )([\d\.]+)', r'(?:.*total )([\d\.]+)', 'result-chpl-stencil-blockdist-*.out'),
):
    dat[name] = {'lognodes': [], 'mflops/s': [], 'walltime': []}
    for filename in sorted(glob.glob(globpat)):
        logn = int(os.path.splitext(filename)[0].split('-')[-1])
        with open(filename) as f:
            text = f.read()
            match = re.search(reflops, text)
            mflopsps = float(match.group(1))
            match = re.search(rewalltime, text)
            walltime = float(match.group(1))
        dat[name]['lognodes'].append(logn)
        dat[name]['mflops/s'].append(mflopsps)
        dat[name]['walltime'].append(walltime)

if args.verbose:
    pprint(dat)

for name in dat.keys():
    dat[name]['lognodes'] = np.array(dat[name]['lognodes'])
    dat[name]['mflops/s'] = np.array(dat[name]['mflops/s'])
    dat[name]['walltime'] = np.array(dat[name]['walltime'])
    dat[name]['efficiency'] = dat[name]['walltime'][0] / dat[name]['walltime']

# plot MFlops/s

plt.clf()

for (name, xy), marker, color in zip(dat.items(), ('M', 'O', 'S', 'B'), ('green+', 'cyan+', 'orange+', 'red+')):
    plt.plot(xy['lognodes'], np.log2(xy['mflops/s']), color=color, marker=args.marker)
    plt.scatter(xy['lognodes'], np.log2(xy['mflops/s']), label=name, color=color, marker=marker, style='bold')

plt.theme(args.theme)
# plt.yticks(np.arange(12, 23, 2))
plt.xticks(np.arange(0, len(xy)))
plt.title("Scaling test")
plt.ylabel("MFlops/s [log2]")
plt.xlabel("number of nodes [log2]")
plt.plotsize(args.width, args.height)
plt.show()

# plot efficiency

plt.clf()

for (name, xy), marker, color in zip(dat.items(), ('M', 'O', 'S', 'B'), ('green+', 'cyan+', 'orange+', 'red+')):
    plt.plot(xy['lognodes'], xy['efficiency'], color=color, marker=args.marker)
    plt.scatter(xy['lognodes'], xy['efficiency'], color=color, marker=marker, style='bold')

plt.theme(args.theme)
plt.ylim(0, 1)
plt.xticks(np.arange(0, len(xy)))
plt.title("Efficiency")
plt.ylabel("Efficiency ~ t0/t")
plt.xlabel("number of nodes [log2]")
plt.plotsize(args.width, args.height)
plt.show()
