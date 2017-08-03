#! /bin/csh
#$ -V
#$ -S /bin/csh
#$ -o /cellar/users/ramarty/Data/ants/sge-system_files
#$ -e /cellar/users/ramarty/Data/ants/sge-system_files
#$ -cwd
#$ -t 1-50
#$ -l h_vmem=10G
#$ -tc 50
#$ -l long
set test_photos=(box61-20170511-0538-00273600 box41-20170318-0359-00100800 box41-20170322-1359-00864000 box41-20170323-0459-00972000 box51-20170512-0307-00432000 box61-20170511-0538-00273600 box41-20170318-0359-00100800 box41-20170322-1359-00864000 box41-20170323-0459-00972000 box51-20170512-0307-00432000 box61-20170511-0538-00273600 box41-20170318-0359-00100800 box41-20170322-1359-00864000 box41-20170323-0459-00972000 box51-20170512-0307-00432000 box61-20170511-0538-00273600 box41-20170318-0359-00100800 box41-20170322-1359-00864000 box41-20170323-0459-00972000 box51-20170512-0307-00432000 box101-01440001 box61-20140125-2110-01454402 box101-01134001 box61-20140119-1410-00367231 box101-00799201 box101-01440001 box61-20140125-2110-01454402 box101-01134001 box61-20140119-1410-00367231 box101-00799201 box101-01440001 box61-20140125-2110-01454402 box101-01134001 box61-20140119-1410-00367231 box101-00799201 box101-01440001 box61-20140125-2110-01454402 box101-01134001 box61-20140119-1410-00367231 box101-00799201 box101-01440001 box61-20140125-2110-01454402 box101-01134001 box61-20140119-1410-00367231 box101-00799201 box101-01440001 box61-20140125-2110-01454402 box101-01134001 box61-20140119-1410-00367231 box101-00799201)
set species_names=(cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah cfellah leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax leptothorax)
set sizes=(30 30 30 30 30 30 30 30 30 30 50 50 50 50 50 50 50 50 50 50 30 30 30 30 30 30 30 30 30 30 50 50 50 50 50 50 50 50 50 50 100 100 100 100 100 100 100 100 100 100)
set steps=(20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20)
set recombinations=(median median median median median mean mean mean mean mean median median median median median mean mean mean mean mean median median median median median mean mean mean mean mean median median median median median mean mean mean mean mean median median median median median mean mean mean mean mean)

set test_photo=$test_photos[$SGE_TASK_ID]
set species_name=$species_names[$SGE_TASK_ID]
set size=$sizes[$SGE_TASK_ID]
set step=$steps[$SGE_TASK_ID]
set recombination=$recombinations[$SGE_TASK_ID]

date
hostname
python /cellar/users/ramarty/Projects/ants/scripts/python/apply_smoothing.py $test_photo $species_name $size $step $recombination
date
