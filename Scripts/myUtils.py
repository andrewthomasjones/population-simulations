import ConfigParser
from functools import reduce

def getVarConf(fName):
    config = ConfigParser.ConfigParser()
    config.read(fName)

    N0 = eval(config.get("var", "N0"))
    #sampCohort = eval(config.get("var", "sampCohort"))
    #sampSize = eval(config.get("var", "sampSize"))
    #try:
    #    sampSNP = eval(config.get("var", "sampSNP"))
    #except:
    #    sampSNP = {}

    numGens = config.getint("sim", "numGens")
    reps = config.getint("sim", "reps")
    dataDir = config.get("sim", "dataDir")

    return N0, numGens, reps, dataDir #sampCohort, sampSize, sampSNP,


def getConfig(fName):
    config = ConfigParser.ConfigParser()
    config.read(fName)

    class Cfg:
        pass

    cfg = Cfg()

    cfg.popSize = config.getint("pop", "popSize")
    cfg.ages = eval(config.get("pop", "ages"))
    if config.has_option("pop", "isMonog"):
        cfg.isMonog = config.getboolean("pop", "isMonog")
    else:
        cfg.isMonog = False
    if config.has_option("pop", "forceSkip"):
        cfg.forceSkip = config.getfloat("pop", "forceSkip") / 100
    else:
        cfg.forceSkip = 0
    if config.has_option("pop", "skip"):
        cfg.skip = eval(config.get("pop", "skip"))
    else:
        cfg.skip = []
    if config.has_option("pop", "litter"):
        cfg.litter = eval(config.get("pop", "litter"))
    else:
        cfg.litter = None
    if config.has_option("pop", "male.probability"):
        cfg.maleProb = config.getfloat("pop", "male.probability")
    else:
        cfg.maleProb = 0.5
    if config.has_option("pop", "gamma.b.male"):
        cfg.doNegBinom = True
        cfg.gammaAMale = eval(config.get("pop", "gamma.a.male"))
        cfg.gammaBMale = eval(config.get("pop", "gamma.b.male"))
        cfg.gammaAFemale = eval(config.get("pop", "gamma.a.female"))
        cfg.gammaBFemale = eval(config.get("pop", "gamma.b.female"))
    else:
        cfg.doNegBinom = False
    cfg.N0 = config.getint("pop", "N0")
    if config.has_option("pop", "survival"):
        cfg.survivalMale = eval(config.get("pop", "survival"))
        cfg.survivalFemale = eval(config.get("pop", "survival"))
    else:
        cfg.survivalMale = eval(config.get("pop", "survival.male"))
        cfg.survivalFemale = eval(config.get("pop", "survival.female"))
    cfg.fecundityMale = eval(config.get("pop", "fecundity.male"))
    cfg.fecundityFemale = eval(config.get("pop", "fecundity.female"))
    if config.has_option("pop", "startLambda"):
        cfg.startLambda = config.getint("pop", "startLambda")
        cfg.lbd = config.getfloat("pop", "lambda")
        # cfg.lbd = mp.mpf(config.get("pop", "lambda"))
    else:
        cfg.startLambda = 99999
        # cfg.lbd = mp.mpf(1.0)
        cfg.lbd = 1.0
    if config.has_option("pop", "Nb"):
        cfg.Nb = config.getint("pop", "Nb")
        cfg.NbVar = config.getfloat("pop", "NbVar")
    else:
        cfg.Nb = None
        cfg.NbVar = None

    cfg.startAlleles = config.getint("genome", "startAlleles")
    cfg.mutFreq = config.getfloat("genome", "mutFreq")
    cfg.numMSats = config.getint("genome", "numMSats")
    if config.has_option("genome", "numSNPs"):
        cfg.numSNPs = config.getint("genome", "numSNPs")
    else:
        cfg.numSNPs = 0

    cfg.reps = config.getint("sim", "reps")
    if config.has_option("sim", "startSave"):
        cfg.startSave = config.getint("sim", "startSave")
    else:
        cfg.startSave = 0
    cfg.gens = config.getint("sim", "gens")
    cfg.dataDir = config.get("sim", "dataDir")

    return cfg

def getAgeFecund(cfg):
    ages = []
    for fec in [cfg.fecundityMale, cfg.fecundityFemale]:
        for i in range(len(fec)):
            if fec[i]>0:
                ages.append(i+1)
                break
    return tuple(ages)


def calcHarmonic(lst):
    #Negatives are converted to infs (LDNe)
    myLst = [x < 0 and float("inf") or x for x in lst]
    try:
        return 1.0 * len(lst) / reduce(lambda x, y: 1.0 / y + x, myLst, 0.0)
    except ZeroDivisionError:
        return None


def getNonGenStats(f):
    l = f.readline()
    stats = []
    while l != '':
        toks = l.rstrip().split(' ')
        try:
            gender = int(toks[3])
            stats.append({
                "gen": int(toks[0]),
                "rep": int(toks[1]),
                "id": int(float(toks[2])),
                "gender": gender,
                "father": int(float(toks[4])),
                "mother": int(float(toks[5])),
                "age": int(float(toks[6])),
            })
        except IndexError:
            break

        l = f.readline()
    return stats


def getDemo(project, model, N0, rep):
    f = open('data/%s/%d%s%d.demo' % (project, N0, model, rep))
    for l in f:
        toks = [x for x in l.strip().rstrip().split(' ') if x != '']
        cycle = int(toks[0])
        gentime = float(toks[1])
        pyramid = [int(x) for x in toks[2:]]
        yield {'cycle': cycle, 'generation': gentime, 'pyramid': pyramid}
    f.close()


def getVk(project, model, N0, rep):
    f = open('data/%s/%d%s%d.vk' % (project, N0, model, rep))
    for l in f:
        toks = [x for x in l.strip().rstrip().split(' ') if x != '']
        cycle = int(toks[0])
        k = float(toks[1])
        vk = float(toks[2])
        nb = float(toks[3])
        ne = float(toks[4])
        yield {'cycle': cycle, 'k': k, 'vk': vk, 'nb': nb, 'ne': ne}
    f.close()
