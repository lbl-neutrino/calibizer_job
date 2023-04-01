#!/usr/bin/env bash
#SBATCH -N 1 --ntasks-per-node=256 -C cpu -L cfs
#SBATCH -t 06:00:00 -A dune -q regular

infile=$1; shift

source load_nompi.sh

logdir=$SCRATCH/logs.calibizer/$(basename "$(dirname "$infile")")
mkdir -p "$logdir"

srun -o "$logdir"/task-%j.%t.out ./module3_worker.py \
    --randsleep 60 --singleshot -c module3_nompi "$infile" "$@"
# srun -o "$logdir"/slurm-%j.%t.out ./module3_worker.py -c module3_nompi "$infile" "$@"
