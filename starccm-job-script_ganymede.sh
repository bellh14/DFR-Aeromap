#!/bin/bash

#SBATCH     --partition=128s
#SBATCH     --nodes=5
#SBATCH     --ntasks=80
#SBATCH     --time=96:00:00
#SBATCH     --mail-type=ALL
#SBATCH     --output=/home/hxb210012/scratch/DOETest1/output.txt

NCPU=80

echo -e "This job allocated $NCPU cpu(s)\nJob is allocated on node(s): $SLURM_JOB_NODELIST" > /home/hxb210012/scratch/DOETest1/batchlog.txt
module load starccm/17.04.007

starccm+ -power -licpath 1999@flex.cd-adapco.com -podkey bP+ffajdHe5WRH/RLQhUAg -batch "/petastore/ganymede/home/hxb210012/DOETest1/DOEMacro.java" -np $NCPU "/petastore/ganymede/home/hxb210012/DOETest1/2024Baseline13in_Straightline_sprung.sim" -bs slurm -time -batch-report
