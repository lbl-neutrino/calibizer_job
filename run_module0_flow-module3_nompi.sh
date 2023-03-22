#!/usr/bin/env bash

outfile=$(realpath $1); shift
chargefile=$(realpath $1); shift
lightfiles=$(realpath $@); shift $#

cd ndlar_flow

yamldir=yamls/module3_flow/workflows

python3 -m h5flow -c \
    $yamldir/charge/charge_event_building.yaml \
    $yamldir/charge/charge_event_reconstruction.yaml \
    $yamldir/combined/combined_reconstruction.yaml \
    -i $chargefile \
    -o $outfile
