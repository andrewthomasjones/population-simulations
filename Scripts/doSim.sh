MODEL=$1
REPS=$2
REPE=$3
DIR=$4

for ((rep=$REPS ; rep<$REPE ; rep++ ))
do
    echo "python sim.py  ${DIR}/${MODEL}.conf >${DIR}/${MODEL}${rep}.sim >${DIR}/${MODEL}${rep}.gen"

    nice -n10 python sim.py  ${DIR}/${MODEL}.conf ${DIR}/${MODEL}${rep}
    while [ $? -ne 0 ]; do
        echo $rep
        nice -n10 python sim.py  ${DIR}/${MODEL}.conf ${DIR}/${MODEL}${rep}
    done
    rm ${DIR}/${MODEL}${rep}.sim.bz2
    rm ${DIR}/${MODEL}${rep}.gen.bz2
    bzip2 ${DIR}/${MODEL}${rep}.sim
    bzip2 ${DIR}/${MODEL}${rep}.gen
    rm ${DIR}/${MODEL}${rep}.sim
    rm ${DIR}/${MODEL}${rep}.gen

done
