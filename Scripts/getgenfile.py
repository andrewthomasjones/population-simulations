from __future__ import print_function
import os
import sys
from doSim import gzip_file, un_gzip_file
from sim import sim
from topGo import write

def getgenfile(reps, repe, model, agedesc, agecond, nindivs = 100, nloci = 100):
    DDIR = "Data" #data directory
    myd = {"DDIR": DDIR, "MODEL": model, "AGECOND": agecond, "AGEDESC": agedesc, "GENS": agecond}

    for rep in range(reps, repe):
        myd["rep"] = rep
        myd["nindivs"] = nindivs
        myd["nloci"] = nloci
        data = un_gzip_file(dir+"/"+model+rep+".sim")
        data2 = sampleIndivsCohort(data, agecond, nindivs, 1, agecond)
        data3 = sampleLoci(data2, dir+"/"+model+rep+".gen", nloci, 100)
        write(ddir+"/ldout/"+model+agedesc+nindivs+nloci+"-"+rep++".txt", data3)


def doSim(model, reps, repe, dir):
    for rep in range(reps, repe):
        sims = sim(dir+"/"+model+".conf")
        write(dir+"/"+model+rep+".sim", sims)
        write(dir+"/"+model+rep+".gen", sims)#???
