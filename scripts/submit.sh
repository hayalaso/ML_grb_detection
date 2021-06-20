#!/bin/sh
#SBATCH --job-name=coincs
#SBATCH --mem-per-cpu=1200mb
#SBATCH --output=logs/simbkg_%A-%a.log
#SBATCH --array=1-1000

NUM_FILE=$((SLURM_ARRAY_TASK_ID+2000))

python simulate_bkg.py -o ../simulation/individual/${NUM_FILE}.csv
