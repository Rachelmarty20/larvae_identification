#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/ants/sge-system_files
#$ -e /cellar/users/ramarty/Data/ants/sge-system_files
#$ -cwd
#$ -t 1-4
#$ -l h_vmem=1G
#$ -tc 4
#$ -l long
set species_names=(cfellah cfellah leptothorax leptothorax)
set sizes=(50 150 50 150)

set species_name=$species_names[$SGE_TASK_ID]
set size=$sizes[$SGE_TASK_ID]

date
hostname
python /cellar/users/ramarty/Projects/ants/scripts/python/build_training.continuous.py $species_name $size
date
