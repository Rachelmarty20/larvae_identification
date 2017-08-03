#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/ants/sge-system_files
#$ -e /cellar/users/ramarty/Data/ants/sge-system_files
#$ -cwd
#$ -t 1-5
#$ -l h_vmem=10G
#$ -tc 4
#$ -l long
set species_names=(cfellah cfellah leptothorax leptothorax leptothorax)
set sizes=(50 30 100 30 50)

set species_name=$species_names[$SGE_TASK_ID]
set size=$sizes[$SGE_TASK_ID]

date
hostname
python /cellar/users/ramarty/Projects/ants/scripts/python/train_classifier.binary.py $species_name $size
date
