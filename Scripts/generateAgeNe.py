import subprocess
import os
import os.path
from os import path
from myUtils import ages, survivalFemale, survivalMale, fecFemale, fecMale
import time



def generateAgeNe(model, N1, outfile, with_bsf):
    survivalFemale[model].append(0)
    survivalMale[model].append(0)
    curr_survival = N1 / 2, N1 / 2
    if path.exists(outfile):
        os.remove(outfile)
    file = open(outfile, 'a')
    file.write(model+ "\n")
    file.write(str(ages[model]-1) + " " + str(N1) +" "+"0.5"+"\n")

    for age in range(ages[model] - 1):
        if with_bsf:
            if curr_survival[0] < 1:
                bf = 0
            else:
                bf = (curr_survival[0] - 1) / curr_survival[0]
            if curr_survival[1] < 1:
                bm = 0
            else:
                bm = (curr_survival[1] - 1) / curr_survival[1]
            curr_survival = curr_survival[0] * survivalFemale[model][age],\
                curr_survival[1] * survivalMale[model][age]
        else:
            bf = bm = 1

        file.write(('%d %f %f %f %f %f %f' % (age + 1, survivalFemale[model][age], fecFemale[model][age], bf,
               survivalMale[model][age], fecMale[model][age], bm)))
        file.write("\n")
    file.close()

def calculateAgeNe(infile, outfile, agene):
    proc = subprocess.Popen([agene],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    proc.stdin.write((infile + "\r\n").encode())
    proc.stdin.write((outfile + "\r\n").encode())
    proc.stdin.flush()
    time.sleep(3)

    try:
        f = open(outfile)
        for l in f:
            if l.find('Ne (Eq 2) ') > -1:
                ne = float(l.rstrip().split(' ')[-1])
            if l.find('Nb ') > -1:
                # We want the last
                nb = float(l.rstrip().split(' ')[-1])
        f.close()
        results = [nb, ne, nb / ne]
    except:
        results = []
    return(results)

#def calculateLDNe(infile, outfile, ldne):
