#!/usr/bin/env bash

infile=$1; shift

logdir=$SCRATCH/logs.calibizer
mkdir -p "$logdir"

sbatch -o "$logdir"/slurm-%j.out "$@" calibizer_job.sh "$infile"
