#!/bin/bash
#SBATCH     --partition=normal
#SBATCH     --nodes=8
#SBATCH     --ntasks=128
#SBATCH     --job-name="AEROMAP"
#SBATCH     --time=96:00:00
#SBATCH     --mail-type=ALL
#SBATCH     --mail-user=hxb210012@utdallas.edu
#SBATCH     --output="output.txt"

WORKING_DIR="/scratch/ganymede/hxb210012/25AeroMapv1"
NCPU=128
PODKEY=""
JAVA_MACRO="AeroMap.java"
SIM_FILE="25AeroMapv1.sim"

module load starccm/17.04.007

starccm+ -power -licpath 1999@flex.cd-adapco.com -podkey $PODKEY -batch $WORKING_DIR/$JAVA_MACRO -np $NCPU $WORKING_DIR/$SIM_FILE -bs slurm -time -batch-report
