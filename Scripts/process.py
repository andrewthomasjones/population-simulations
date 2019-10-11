from __future__ import division, print_function
import os
import subprocess
import sys
import time
import os.path as path
import ntpath

from doSim import doSim
from totalAll import totalAll
from demo import demo
from nb3 import nb3
from doSim import write
from generateAgeNe import generateAgeNe,calculateAgeNe

main_dir = path.abspath((path.join(__file__ ,"../..")))
agene = main_dir + '/bin/AgeNeV2.exe'
infile = "tmp.agene"
outfile = "out.tmp"


infile1 = (main_dir + '/Output/' + infile)
infile2 = (main_dir + '/Output/' + infile).replace(os.sep,ntpath.sep)
outfile2 = (main_dir + '/Output/' + outfile).replace(os.sep,ntpath.sep)

print(infile2)
print(outfile2)

model = "grizzly"
N1 = 100
with_bsf = ""

#AgeNe interactions
generateAgeNe(model, N1, infile1,  'yes' if with_bsf else '')
ratio = calculateAgeNe(infile2, outfile2, agene)
print(ratio)

doSim("100grizzly", 0, 2, "Output")
totalAll("Output/var-100grizzly.conf")
demo_1 = demo( Data/var-100grizzly.conf)
write("Output/demo.txt", demo_1)
nb3_1 = nb3(Data/var-100grizzly.conf)
write("Output/demo.txt", nb3_1)
totalAll("Output/var-100grizzly.conf", "gen")

# python generateAgeNe.py grizzly 100 #good
# bash doSim.sh 100grizzly 0 2 Data
# python totalAll.py Data/var-100grizzly.conf
# python demo.py Data/var-100grizzly.conf > demo.txt
# python nb3.py Data/var-100grizzly.conf > ne3.txt #here
# python totalAll.py Data/var-100grizzly.conf gen #here
