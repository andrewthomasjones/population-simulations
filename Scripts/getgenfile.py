from __future__ import print_function
import os
import sys


## Setup
reps = int(sys.argv[1])
repe = int(sys.argv[2])
model = sys.argv[3]
agedesc = sys.argv[4] # the name of the sampling strategy for naming purposes
agecond = sys.argv[5] # the max age to sample

DDIR = "Data" #data directory
myd = {"DDIR": DDIR, "MODEL": model,
       "AGECOND": agecond, "AGEDESC": agedesc, "GENS": agecond}
nindivs = 100

for rep in range(reps, repe):
    myd["rep"] = rep
    myd["nindivs"] = 100
    myd["nloci"] = 100
    #os.system('bzcat {DDIR}/{MODEL}{rep}.sim.bz2 |python sampleIndivsCohort.py {AGECOND} {nindivs} 1 {GENS} > {DDIR}/ldout/{MODEL}{AGEDESC}{nindivs}{nloci}-{rep}'.format(**myd))
    os.system('bzcat {DDIR}/{MODEL}{rep}.sim.bz2 | python sampleIndivsCohort.py {AGECOND} {nindivs} 1 {GENS} |python sampleLoci.py {DDIR}/{MODEL}{rep}.gen.bz2 {nloci} 100  > {DDIR}/ldout/{MODEL}{AGEDESC}{nindivs}{nloci}-{rep}.txt'.format(**myd))
