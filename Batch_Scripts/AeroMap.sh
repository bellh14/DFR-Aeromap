!/bin/bash

#SBATCH --partition=256i
#SBATCH --nodes=4
#SBATCH --ntasks=80
#SBATCH --time=96:00:00
#SBATCH --mail-type=ALL
#SBATCH --output=/home/hxb210012/scratch/NewMapTest/batch_1.out

NCPU=80
PODKEY=""

echo -e "This job allocated $NCPU cores\nJob is allocated on node(s): $SLURM_JOB_NODELIST" > /home/hxb210012/scratch/NewMapTest/batch_1_log.out

module load starccm/17.04.007

starccm+ -power -licpath 1999@flex.cd-adapco.com -podkey $PODKEY -batch "/petastore/ganymede/home/hxb210012/scratch/NewMapTest/batch_1/HeaveSweep.java"