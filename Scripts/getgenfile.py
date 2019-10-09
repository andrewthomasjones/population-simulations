from __future__ import print_function
import os
import sys

def getgenfile(reps, repe, model, agedesc, agecond, nindivs = 100, nloci = 100):

    DDIR = "Data" #data directory
    myd = {"DDIR": DDIR, "MODEL": model, "AGECOND": agecond, "AGEDESC": agedesc, "GENS": agecond}
    
    for rep in range(reps, repe):
        myd["rep"] = rep
        myd["nindivs"] = nindivs
        myd["nloci"] = nloci
        #os.system('bzcat {DDIR}/{MODEL}{rep}.sim.bz2 |python sampleIndivsCohort.py {AGECOND} {nindivs} 1 {GENS} > {DDIR}/ldout/{MODEL}{AGEDESC}{nindivs}{nloci}-{rep}'.format(**myd))
        os.system('bzcat {DDIR}/{MODEL}{rep}.sim.bz2 | python sampleIndivsCohort.py {AGECOND} {nindivs} 1 {GENS} |python sampleLoci.py {DDIR}/{MODEL}{rep}.gen.bz2 {nloci} 100  > {DDIR}/ldout/{MODEL}{AGEDESC}{nindivs}{nloci}-{rep}.txt'.format(**myd))
