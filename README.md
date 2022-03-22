# MEDYAN

[![Build Status](https://github.com/medyan-dev/MEDYAN/workflows/build/badge.svg)](https://github.com/medyan-dev/MEDYAN/actions)
[![docs](https://img.shields.io/badge/docs-stable-blue.svg)](http://medyan.org/docs/site/index.html)
[![website](https://img.shields.io/website?down_message=medyan.org&up_message=medyan.org&url=http%3A%2F%2Fmedyan.org)](http://medyan.org)

Welcome to Papoian Lab’s *Mechanochemical Dynamics of Active Networks* software package.

Copyright 2015-2022, Papoian lab at the University of Maryland.

For more general information about the code, visit [medyan.org](http://medyan.org) or the [Papoian lab page](http://papoian.chem.umd.edu/). 

This code is distributed under [the license](license.txt) found in this directory, `license.txt`.


## Usage

The MEDYAN executable can to be built from source. Check the [installation guide](docs/manual/installation.md) for more information.

After compilation, MEDYAN can be invoked with additional command line arguments. Use `./medyan -h` to see the help message, which includes all the available commands and options.

To run a simulation with a given system input file, run

```console
./medyan -s <system-input-file> [-i <input-directory>] [-o <output-directory>]
```

The input files are described in detail [here](docs/manual/input-files.md). Example input files for various systems are provided in the `examples` directory. The additional referenced input files are looked up in the same directory as the system input file, unless the `-i` option is used to specify a different directory.

The simulation output is written to the current working directory unless the `-o` option is used to specify a different directory. The output files are described in detail [here](docs/manual/output-files.md).

MEDYAN also comes with a native interactive visualization tool to display simulation trajectories. Run `./medyan gui` to launch MEDYAN in visualization-only mode. In this mode, one can press <kbd>g</kbd> to toggle the GUI overlay.


## Authors

Active developers:

| Name                    | Email             |
|-------------------------|-------------------|
| Haoran Ni               | haoranni@umd.edu  |
| Nathan Zimmerberg       | nzimmerb@umd.edu  |

All developers:

Garegin Papoian (gpapoian@umd.edu), Konstantin Popov, James Komianos, Aravind Chandrasekaran, Qin Ni, Carlos Floyd, Haoran Ni, Nathan Zimmerberg, Joshua Lucker.

All general correspondence about the code and its applications should be directed to Garegin Papoian. All developer and more specific code, installation, and usage correspondence should be directed to Active developers via email or the issue tracker.


## Files

This MEDYAN distribution has the following files and directories:

| File/Dir        | Description                 |
|-----------------|-----------------------------|
| docs            | Documentation files         |
| examples        | A packaged example          |
| external        | External libraries used by MEDYAN |
| license.txt     | Code licensing information  |
| papers          | Relevant papers             |
| README.md       | Current file                |
| restart         | Restart scripts             |
| src             | All source files            |
| visual          | Visualization scripts       |

See the following documentation for details:

| Documentation file      | Description |
|-------------------------|-------------|
| [docs/manual/installation.md](docs/manual/installation.md) | Tips on compilation, etc |
| [docs/manual/input-files.md](docs/manual/input-files.md)   | Tips on input files |
| [docs/manual/output-files.md](docs/manual/output-files.md)   | Tips on output files |
| [docs/ExampleGuide.pdf](docs/ExampleGuide.pdf) | Packaged example description |
