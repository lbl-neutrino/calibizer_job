#!/usr/bin/env bash

infile=$1; shift

logdir=$SCRATCH/logs.calibizer/$(basename "$(dirname "$infile")")
mkdir -p "$logdir"

sbatch -o "$logdir"/job-%j.out "$@" calibizer_job_nompi.sh "$infile"
