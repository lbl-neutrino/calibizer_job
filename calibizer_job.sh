#!/usr/bin/env bash
#SBATCH -N 1 --ntasks-per-node=256 -C cpu -L cfs
#SBATCH -t 01:00:00 -A dune -q regular

source load.sh

./calibizer_worker.py "$@"
