#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/ants/sge-system_files/
#$ -e /cellar/users/ramarty/Data/ants/sge-system_files/
#$ -cwd
#$ -l h_vmem=1G
#$ -l long
date
hostname
python /cellar/users/ramarty/Projects/ants/scripts/python/version3.0/create_training.py
date
