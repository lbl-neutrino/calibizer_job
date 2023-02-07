#!/usr/bin/env bash

chargefile=$(realpath $1)
lightfile=$(realpath $2)
outfile=$(realpath $3)

logdir=$SCRATCH/logs.calibizer/$SLURM_JOBID
mkdir -p "$logdir"

cd module0_flow

yamldir=module3_yamls/workflows

# srun -o "$logdir"/slurm-%j.%t.out \
#     python3 -m h5flow -c $yamldir/charge/charge_event_building.yaml \
#     $yamldir/charge/charge_event_reconstruction.yaml \
#     $yamldir/combined/combined_reconstruction.yaml \
#     -i "$infile" \
#     -o "$outfile"

# srun -n 256 \
#     python3 -m h5flow -c \
#     $yamldir/light/light_event_building_adc64.yaml \
#     $yamldir/light/light_event_reconstruction.yaml \
#     -i $lightfile \
#     -o $outfile

srun -n 256 \
    python3 -m h5flow -c \
    $yamldir/light/light_event_building_adc64.yaml \
    $yamldir/light/light_event_reconstruction-keep_wvfm.yaml \
    -i $lightfile \
    -o $outfile

# srun -n 256 \
#     python3 -m h5flow -c \
#     $yamldir/charge/charge_event_building.yaml \
#     $yamldir/charge/charge_event_reconstruction.yaml \
#     $yamldir/charge/charge_light_association.yaml \
#     $yamldir/combined/combined_reconstruction.yaml \
#     -i $chargefile \
#     -o $outfile

srun -n 256 \
    python3 -m h5flow -c \
    $yamldir/charge/charge_event_building.yaml \
    $yamldir/charge/charge_event_reconstruction.yaml \
    $yamldir/charge/charge_light_assoc.yaml \
    $yamldir/combined/combined_reconstruction.yaml \
    -i $chargefile \
    -o $outfile
