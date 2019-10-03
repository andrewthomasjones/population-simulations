from __future__ import division, print_function

import os
import subprocess
import sys
import time
from generateAgeNe import generateAgeNe,calculateAgeNe
import os.path as path

main_dir = path.abspath((path.join(__file__ ,"../..")))
agene = main_dir + '\\bin\\AgeNeV2.exe'
infile = "tmp.agene"
outfile = "out.tmp"

infile2 = main_dir + '\\bin\\' + infile
outfile2 = main_dir + '\\bin\\' + outfile


model = "grizzly"
N1 = 100
with_bsf = ""

generateAgeNe(model, N1, infile2,  'yes' if with_bsf else '')
ratio = calculateAgeNe(infile, outfile, agene)

print(ratio)
