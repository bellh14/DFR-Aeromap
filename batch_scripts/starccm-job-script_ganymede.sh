#!/bin/bash

#SBATCH     --partition=smallmem
#SBATCH     --nodes=10
#SBATCH     --ntasks=80
#SBATCH     --time=96:00:00
#SBATCH     --mail-type=ALL
#SBATCH     --output=/home/hxb210012/scratch/yaw_angle/output.txt

NCPU=80

echo -e "This job allocated $NCPU cpu(s)\nJob is allocated on node(s): $SLURM_JOB_NODELIST" > /home/hxb210012/scratch/yaw_angle/batchlog.txt
module load starccm/17.04.007

starccm+ -power -licpath 1999@flex.cd-adapco.com -podkey <podkey> -batch "/petastore/ganymede/home/hxb210012/yaw_angle/YawAngleDOE.java" -np $NCPU "/petastore/ganymede/home/hxb210012/yaw_angle/2024Baseline13in_Straightline_sprung.sim" -bs slurm -time -batch-report
