# Apptainer/Singularity Definition Files

This directory contains a number of `.def` Apptainer definition files for building the Apptainer `.sif` files found in releases. On linux computers with Apptainer or Singularity installed and with compatible architecture, the `.sif` files can be run as if they are compiled medyan executables.

Always test the container with for example `./medyan-5.4.0-avx2 test` to ensure it is compatible.

If you want to use the medyan gui, or your architecture isn't compatible, check the [installation guide](../docs/manual/installation.md) to compile medyan from source.

To build the containers from the def files run for example.

```sh
apptainer build --writable-tmpfs medyan-5.4.0-avx2.sif medyan-5.4.0-avx2.def
```

# Using Apptainer/Singularity Containers on an HPC cluster.

The following is an example of how to install and run medyan 5.4.0 on the UMD Zaratan HPC cluster.


```sh
module load singularity
wget https://github.com/medyan-dev/medyan-public/releases/download/v5.4.0/medyan-5.4.0-avx2.sif
chmod +x medyan-5.4.0-avx2.sif
./medyan-5.4.0-avx2.sif test
```