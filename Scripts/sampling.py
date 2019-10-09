from __future__ import print_function
from sys import stdin, stderr, argv, exit
import random
import bz2
import random

def sampleIndivs(cond, nindivs, startGen, endGen):

    if(nindivs == "ALL"):
        nindivs = None  # Actually we stop at 200
        maxInds = 200

        lp=True

        l = stdin.readline()

        # currGen = cfg.startSave
        currGen = 0

        indivs = []
    while l != "":
        toks = l.rstrip().split(" ")
        rep = int(float(toks[1]))
        if rep > 0:
            break
        gen = int(float(toks[0]))
        id = int(float(toks[2]))
        sex = int(float(toks[3]))
        father = int(float(toks[4]))
        mother = int(float(toks[5]))
        age = int(float(toks[6]))

        if gen > currGen:
            if currGen >= startGen:
                if nindivs:
                    print(currGen, random.sample(indivs, nindivs))
                else:
                    if len(indivs) > maxInds:
                        print(currGen, random.sample(indivs, maxInds))
                    else:
                        print(currGen, indivs)
                if lp:
                    if nindivs:
                        print(random.sample(indivs, nindivs))
                    else:
                        if len(indivs) > maxInds:
                            print(random.sample(indivs, maxInds))
                        else:
                            print(indivs)
            indivs = []
            currGen = gen
            if currGen > endGen:
                break
        if eval(cond):
            indivs.append(id)
        l = stdin.readline()
    if currGen <= endGen:
        if nindivs:
            print(currGen, random.sample(indivs, nindivs))
        else:
            if len(indivs) > maxInds:
                print(currGen, random.sample(indivs, maxInds))
            else:
                print(currGen, indivs)
        if lp:
            if nindivs:
                print(random.sample(indivs, nindivs))
            else:
                if len(indivs) > maxInds:
                    print(random.sample(indivs, maxInds))
                else:
                    print(indivs)


def sampleLoci(genFile, nLoci, maxLoci, startLoci = 0):

    loci = [x + startLoci for x in random.sample(list(range(maxLoci)), nloci)]

    l = stdin.readline()
    gens = []

    currGen = 0

    # get individuals per generation
    indivs = set()
    while l != "":
        l = l.rstrip()
        point = l.find(" ")
        print("point", point)
        gen = l[:point]
        print("gen", gen)
        genIndivs = eval(l[point:])
        indivs = indivs.union(genIndivs)
        gens.append(genIndivs)
        l = stdin.readline()

    # get genetic data
    f = bz2.open(genFile, 'rt')
    l = f.readline()
    genetics = {}
    while l != "":
        toks = l.rstrip().split(" ")
        id = int(float(toks[0]))
        gen = int(float(toks[1]))
        myAlleles = toks[2:]
        if id in indivs:
            myloci = []
            for locus in loci:
                myloci.append(myAlleles[locus])
            genetics[id] = myloci
        l = f.readline()
    f.close()

    # dump genepop file
    print("lala land")
    for locus in loci:
        print("l" + str(locus))
    for indivs in gens:
        print("Pop")
        for indiv in indivs:
            print("i" + str(indiv) + ",", end=' ')
            print(" ".join(genetics[indiv]))



def getSibs(sameParents, todo):
    rels = []
    done_parents = []
    while todo > 0:
        have_more = False
        for parents, vals in sameParents.items():
            if parents in done_parents:
                continue
            done_parents.append(parents)
            if len(vals) > 1:
                have_more = True
                rels.append(vals[0])
                rels.append(vals[1])
                todo -= 2
                break
        if not have_more:
            print("Not enough relateds")
            exit()
    return rels




def sampleIndivsRelated( frac, nindivs, startGen, endGen):

    frac = int(argv[1]) / 100
    if(nindivs == "ALL"):
        nindivs = None  # Actually we stop at 200
        maxInds = 200

    l = stdin.readline()

    currGen = 0

    sameParents = {}
    indivs = []
    while l != "":
        toks = l.rstrip().split(" ")
        rep = int(float(toks[1]))
        if rep > 0:
            break
        gen = int(float(toks[0]))
        id = int(float(toks[2]))
        sex = int(float(toks[3]))
        father = int(float(toks[4]))
        mother = int(float(toks[5]))
        age = int(float(toks[6]))
        if age > 1:
            l = stdin.readline()
            continue
        sameParents.setdefault((father, mother), []).append(id)
        # sameParents.setdefault(father, []).append(id)
        # sameParents.setdefault(mother, []).append(id)
        indivs.append(id)

        if gen > currGen:
            if currGen >= startGen:
                relateds = getSibs(sameParents, frac * nindivs)
                for related in relateds:
                    indivs.remove(related)
                if nindivs:
                    remaining = nindivs - len(relateds)
                    print(currGen, relateds + random.sample(indivs, remaining))
                else:
                    if len(indivs) > maxInds:
                        remaining = maxInds - len(relateds)
                        print(currGen, relateds + random.sample(indivs, remaining))
                    else:
                        print(currGen, relateds + indivs)
            sameParents = {}
            indivs = []
            currGen = gen
            if currGen > endGen:
                break

        l = stdin.readline()

    if currGen <= endGen:
        relateds = getSibs(sameParents, frac * nindivs)
        for related in relateds:
            indivs.remove(related)
        if nindivs:
            remaining = nindivs - len(relateds)
            print(currGen, relateds + random.sample(indivs, remaining))
        else:
            if len(indivs) > maxInds:
                remaining = maxInds - len(relateds)
                print(currGen, relateds + random.sample(indivs, remaining))
            else:
                print(currGen, relateds + indivs)

def getIndivs(ageInds):
    indivs = []
    maxIndsPerCohort = min([len(x) for x in list(ageInds.values())])
    for age, inds in list(ageInds.items()):
        indivs.extend(random.sample(inds, maxIndsPerCohort))
    return indivs

def sampleIndivsCohort(maxAge, nindivs, startGen, endGen):

    if(nindivs == "ALL"):
        nindivs = None  # Actually we stop at 200
        maxInds = 200

        lp=True

        l = stdin.readline()

    # currGen = cfg.startSave
    currGen = 0

    ageCnt = {}
    indivsAge = {}
    while l != "":
        toks = l.rstrip().split(" ")
        rep = int(float(toks[1]))
        if rep > 0:
            break
        gen = int(float(toks[0]))
        id = int(float(toks[2]))
        sex = int(float(toks[3]))
        father = int(float(toks[4]))
        mother = int(float(toks[5]))
        age = int(float(toks[6]))


        if gen > currGen:
            if currGen >= startGen:
                indivs = getIndivs(indivsAge)
                if nindivs:
                    print(currGen, random.sample(indivs, nindivs))
                else:
                    if len(indivs) > maxInds:
                        print(currGen, random.sample(indivs, maxInds))
                    else:
                        print(currGen, indivs)
                if lp:
                    if nindivs:
                        print(random.sample(indivs, nindivs))
                    else:
                        if len(indivs) > maxInds:
                            print(random.sample(indivs, maxInds))
                        else:
                            print(indivs)
            indivsAge = {}
            currGen = gen
            if currGen > endGen:
                break

        if age <= maxAge:
            ## added
            #print(age) # checking age
            ageCnt[age] = ageCnt.get(age, 0) + 1
            indivsAge.setdefault(age, []).append(id)
        l = stdin.readline()
    if currGen <= endGen:
        indivs = getIndivs(indivsAge)
        if nindivs:
            print(currGen, random.sample(indivs, nindivs))
        else:
            if len(indivs) > maxInds:
                print(currGen, random.sample(indivs, maxInds))
            else:
                print(currGen, indivs)
        if lp:
            if nindivs:
                print(random.sample(indivs, nindivs))
            else:
                if len(indivs) > maxInds:
                    print(random.sample(indivs, maxInds))
                else:
                    print(indivs)
