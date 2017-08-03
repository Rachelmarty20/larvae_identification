#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/ants/sge-system_files/
#$ -e /cellar/users/ramarty/Data/ants/sge-system_files/
#$ -cwd
#$ -t 1-35
#$ -l h_vmem=16G
#$ -tc 10
#$ -l long
set learnings=(0.001 0.01 0.1 1 10 100 1000 0.001 0.01 0.1 1 10 100 1000 0.001 0.01 0.1 1 10 100 1000 0.001 0.01 0.1 1 10 100 1000 0.001 0.01 0.1 1 10 100 1000)
set batches=(1 1 1 1 1 20 20 20 20 20 100 100 100 100 100 500 500 500 500 500 1000 1000 1000 1000 1000)

set learning=$learnings[$SGE_TASK_ID]
set batch=$batches[$SGE_TASK_ID]

date
hostname
python /cellar/users/ramarty/Projects/ants/scripts/python/version3.0/parameter_sweep.v1.py $learning $batch
date
