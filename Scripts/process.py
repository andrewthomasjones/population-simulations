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

infile2 = main_dir + '\\Output\\' + infile
outfile2 = main_dir + '\\Output\\' + outfile

model = "grizzly"
N1 = 100
with_bsf = ""

#AgeNe interactions
generateAgeNe(model, N1, infile2,  'yes' if with_bsf else '')
ratio = calculateAgeNe(infile2, outfile2, agene)
print(ratio)

#Simulations
