from __future__ import print_function
import os
import sys
from nongen import nongen
from ofs import ofs

def un_gzip_file(fileName):
    fp = open(fileName, "wb")
    with gzip.open(fileName+".gz", "rb") as f:
	       bindata = f.read()
    fp.write(bindata)
    fp.close()

def write(fileName, data):
    fp = open(fileName, "wb")
    fp.write(data)
    fp.close()

def toGo(reps, repe, model, dir, startgen, endgen, matureage, ddir):
    for rep in range(reps, repe):
      un_gzip_file(ddir + "/" + model + rep + ".sim") #also send to nongen?
      nongen(ddir + "/" + model + rep + ".demo",  ddir + "/" + model + rep + ".bree")
      un_gzip_file(ddir + "/" + model + rep + ".sim") #also send to ofs?
      ofs.py(ddir + "/" + model + rep + ".ofs")
      cat(ddir + "/" + model + rep + ".ofs")
      vk1 = vk(ddir + "/" + model + rep + ".demo", startgen, endgen)
      write(ddir + "/" + model + rep + ".vk", vk1)
      cat(ddir + "/" + model + rep + ".ofs")
      vk_mature = vk(ddir + "/" + model + rep + ".demo", startgen, endgen, matureage)
      write(ddir + "/" + model + rep + ".vk.mature", vk_mature)
