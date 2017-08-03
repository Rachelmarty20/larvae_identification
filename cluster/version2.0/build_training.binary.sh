#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/ants/sge-system_files
#$ -e /cellar/users/ramarty/Data/ants/sge-system_files
#$ -cwd
#$ -t 1-2
#$ -l h_vmem=1G
#$ -tc 4
#$ -l long
set species_names=(cfellah leptothorax)
set sizes=(50 50)

set species_name=$species_names[$SGE_TASK_ID]
set size=$sizes[$SGE_TASK_ID]

date
hostname
python /cellar/users/ramarty/Projects/ants/scripts/python/build_training.binary.py $species_name $size
date
