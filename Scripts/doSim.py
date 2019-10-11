import bz2
import os
from sim import sim
import gzip

def gzip_file(fileName):
    fp = open(fileName,"rb")
    data = fp.read()
    bindata = bytearray(data)
    with gzip.open(fileName+".gz", "wb") as f:
	       f.write(bindata)

def un_gzip_file(fileName):
    fp = open(fileName, "wb")
    with gzip.open(fileName+".gz", "rb") as f:
	       bindata = f.read()
    fp.write(bindata)
    fp.close()

def doSim(model, reps, repe, dir):

  for rep in range(reps, repe):

    print("python sim.py  " dir + "/" + model + ".conf" > dir + "/" + model + rep + ".sim" > dir + "/" + model + rep + ".gen")
    cfg = (dir + "/" +model + ".conf" dir + "/" +model + rep)
    prefOut = (dir + "/" +model + ".conf" dir + "/" +model + rep)
    sim = sim(cfg, prefOut)

    os.remove(dir + "/" + model + rep + ".sim.bz2")
    os.remove(dir + "/" + model + rep + ".gen.bz2")
    gzip_file(dir + "/" + model + rep + ".sim")
    gzip_file(dir + "/" + model + rep + ".gen")
    os.remove(dir + "/" + model + rep + ".sim")
    os.remove(dir + "/" + model + rep + ".gen")
