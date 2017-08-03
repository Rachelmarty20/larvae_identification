#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/ants/sge-system_files
#$ -e /cellar/users/ramarty/Data/ants/sge-system_files
#$ -cwd
#$ -t 1-48
#$ -l h_vmem=40G
#$ -tc 50
#$ -l long
set species_names=(cfellah cfellah cfellah cfellah cfellah cfellah leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax cfellah cfellah cfellah cfellah cfellah cfellah leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax cfellah cfellah cfellah cfellah cfellah cfellah leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax cfellah cfellah cfellah cfellah cfellah cfellah leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax)
set sizes=(50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50 50)
set batch_sizes=(10 10 10 10 10 10 10 10 10 10 10 10 50 50 50 50 50 50 50 50 50 50 50 50 100 100 100 100 100 100 100 100 100 100 100 100 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000)
set learning_rates=(0.001 0.01 0.1 1 10 100 0.001 0.01 0.1 1 10 100 0.001 0.01 0.1 1 10 100 0.001 0.01 0.1 1 10 100 0.001 0.01 0.1 1 10 100 0.001 0.01 0.1 1 10 100 0.001 0.01 0.1 1 10 100 0.001 0.01 0.1 1 10 100)

set species_name=$species_names[$SGE_TASK_ID]
set size=$sizes[$SGE_TASK_ID]
set batch_size=$batch_sizes[$SGE_TASK_ID]
set learning_rate=$learning_rates[$SGE_TASK_ID]

date
hostname
python /cellar/users/ramarty/Projects/ants/scripts/python/version4.0/train_classifier.py $species_name $size $batch_size $learning_rate
date
