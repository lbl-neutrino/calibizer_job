# Installing

Run `install.sh`, which will set up the `module0_flow_env` conda environment in
`~/.conda/envs` and download `module0_flow` here.

If necessary, edit `module0_flow/module2_yamls/reco/charge/HitBuilder.yaml` and
change the `pedestal_file` to the right, erm, pedestal file.

If you ran `install.sh` on Perlmutter, the conda env won't work on Cori, and
vice versa. So if you're using more than one cluster, rename `module0_flow_env`
in `install.sh` and `load.sh`, as necessary.


# Grabbing a node

Perlmutter:

``` bash
salloc -q interactive -A dune -C cpu -t 240 --ntasks-per-node=256
```

Cori Haswell:

``` bash
salloc -q interactive -A dune -C haswell -t 240 --ntasks-per-node=64
```

Cori KNL:

``` bash
salloc -q interactive -A dune -C knl -t 240 --ntasks-per-node=272
```


# Environment setup

``` bash
source load.sh
```

Not necessary if you're just submitting batch jobs.


# Launching a worker interactively

From a compute node provided by `salloc`:

``` bash
./calibizer_worker.py /path/to/input.txt
```

where `input.txt` contains a list of packet files to process. The output
directory is configured at the top of `calibizer_worker.py`.


# Submitting batch jobs

``` bash
./submit_calibizer.sh /path/to/input.txt [extra sbatch args...]
```

This calls `sbatch` to submit `calibizer_job.sh`. The latter has some
Perlmutter-specific `SBATCH` directives, so if running on Cori, you will want to
override them when calling `submit_calibizer.sh`.

Each individual job processes one file at a time, with the workload spread over
all available cores using MPI. On Cori, you can allocate multiple nodes to a job
using the `-N` option to `sbatch`. However, on Perlmutter, doing so will cause
the job will crash somewhere in h5py or MPICH &#x2013; this needs to be investigated!
For now, stick with single-node jobs on Perlmutter.

To process multiple files in parallel, use a job array, e.g. by passing the
`sbatch` option `--array=1-5`.

Logs will go in `$SCRATCH/logs.calibizer`.


# Examples: Manually invoking h5flow

## Module 2

``` bash
cd module0_flow

srun --ntasks-per-node=256 \
    h5flow -c module2_yamls/workflows/charge/charge_event_building.yaml \
    module2_yamls/workflows/charge/charge_event_reconstruction.yaml \
    module2_yamls/workflows/gen_all_resources.yaml \
    -i /global/cfs/cdirs/dune/www/data/Module2/TPC12_run2/selftrigger-run2-packet-2022_11_29_22_31_CET.h5 \
    -o ~/dunescratch/data/selftrigger-run2-reco-2022_11_29_22_31_CET.h5
```

## Module 3

``` bash
srun --ntasks-per-node=256 \
    python3 -m h5flow -c module3_yamls/workflows/charge/charge_event_building.yaml \
    module3_yamls/workflows/charge/charge_event_reconstruction.yaml \
    module3_yamls/workflows/combined/combined_reconstruction.yaml \
    -i /some/packet.h5 \
    -o /some/reco.h5
```

In the event of trouble, try omitting the `combined_reconstruction.yaml`. In the
event of further trouble, try creating
`module3_yamls/workflows/gen_all_resources.yaml`, based on
`module2_yamls/workflows/gen_all_resources.yaml`, with the module2-specific
paths replaced with their module3-specific equivalents.
