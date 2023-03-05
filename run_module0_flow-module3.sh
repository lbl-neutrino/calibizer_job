#!/usr/bin/env bash

outfile=$(realpath $1); shift
chargefile=$(realpath $1); shift
lightfiles=$(realpath $@); shift $#

[[ "$NERSC_HOST" == "cori" ]] && on_cori=true || on_cori=false

$on_cori && ntasks=64 || ntasks=256
echo "ntasks = $ntasks"

logdir=$SCRATCH/logs.calibizer/$SLURM_JOBID
mkdir -p "$logdir"

cd ndlar_flow

yamldir=yamls/module3_flow/workflows

# srun -o "$logdir"/slurm-%j.%t.out \
#     python3 -m h5flow -c $yamldir/charge/charge_event_building.yaml \
#     $yamldir/charge/charge_event_reconstruction.yaml \
#     $yamldir/combined/combined_reconstruction.yaml \
#     -i "$infile" \
#     -o "$outfile"

# srun -n $ntasks \
#     python3 -m h5flow -c \
#     $yamldir/light/light_event_building_adc64.yaml \
#     $yamldir/light/light_event_reconstruction.yaml \
#     -i $lightfile \
#     -o $outfile

# srun -n $ntasks \
#     python3 -m h5flow -c \
#     $yamldir/charge/charge_event_building.yaml \
#     $yamldir/charge/charge_event_reconstruction.yaml \
#     $yamldir/charge/charge_light_association.yaml \
#     $yamldir/combined/combined_reconstruction.yaml \
#     -i $chargefile \
#     -o $outfile

# srun -o "$logdir"/slurm-%j.%t.out -n $ntasks \
#     python3 -m h5flow -c \
#     $yamldir/light/light_event_building_adc64.yaml \
#     $yamldir/light/light_event_reconstruction-keep_wvfm.yaml \
#     -i $lightfile \
#     -o $outfile

for lightfile in $lightfiles; do
    srun --open-mode=append -o "$logdir"/slurm-%j.%t.out --ntasks-per-node $ntasks \
        python3 -m h5flow -c \
        $yamldir/light/light_event_building_adc64.yaml \
        $yamldir/light/light_event_reconstruction.yaml \
        -i $lightfile \
        -o $outfile
done

cp $outfile ${outfile%.h5}.bak.h5

# srun --open-mode=append -o "$logdir"/slurm-%j.%t.out --ntasks-per-node $ntasks \
#     python3 -m h5flow -c \
#     $yamldir/charge/charge_event_building.yaml \
#     $yamldir/charge/charge_event_reconstruction.yaml \
#     $yamldir/charge/charge_light_assoc.yaml \
#     $yamldir/combined/combined_reconstruction.yaml \
#     -i $chargefile \
#     -o $outfile

srun --open-mode=append -o "$logdir"/slurm-%j.%t.out --ntasks-per-node $ntasks \
    python3 -m h5flow -c \
    $yamldir/charge/charge_event_building.yaml \
    -i $chargefile \
    -o $outfile

cp $outfile $outfile.1.h5

srun --open-mode=append -o "$logdir"/slurm-%j.%t.out --ntasks-per-node $ntasks \
    python3 -m h5flow -c \
    $yamldir/charge/charge_event_reconstruction.yaml \
    -i $outfile.1.h5 \
    -o $outfile

cp $outfile $outfile.2.h5

srun --open-mode=append -o "$logdir"/slurm-%j.%t.out --ntasks-per-node $ntasks \
    python3 -m h5flow -c \
    $yamldir/charge/charge_light_assoc.yaml \
    -i $outfile.2.h5 \
    -o $outfile

cp $outfile $outfile.3.h5

# XXX tracklet reco disabled

srun --open-mode=append -o "$logdir"/slurm-%j.%t.out --ntasks-per-node $ntasks \
    python3 -m h5flow -c \
    $yamldir/combined/combined_reconstruction.yaml \
    -i $outfile.3.h5 \
    -o $outfile
