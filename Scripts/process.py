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

#1. I run this line to get the demographic data I need to input into the myUtils ect so that the code has the information it needs to make the simulated data, where grizzly is the name of the model, and 100 is the number of N1 (year of the young) offspring I want.
#python generateAgeNe.py grizzly 100

# 3.  I do the sims using this (20 reps)
#      $ bash doSim.sh 100grizzly 0 20 Data

# 4. Then I calculate the demographic data from the sims using this.. ** this all looks ok up to this point
#      $ python totalAll.py Data/var-100grizzly.conf

# 5. Now I can get the stats from the gen and sim files directly
#      $ python demo.py Data/var-100grizzly.conf > demo.txt.

# ** this is ok too, the stats calculated directly from demographic data
#      $ python nb3.py Data/var-100grizzly.conf > ne3.txt                         ** this is not ok! From my understanding this is calculated from the simulated data itself….

# 6. Then using the simulated genetic data I make a file using this to put into NeEstimator directly
#      $ python totalAll.py Data/var-100grizzly.conf gen                             ** this is not ok, but the same of the ne3.txt
