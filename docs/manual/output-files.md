# Output files

MEDYAN can produce a number of output types, set in the `SystemFile`, produced at a
snapshot frequency also defined in the `SystemFile`. These output files will be placed in the
`OutputDirectory` specified at runtime. The output types are described below.

## snapshot.traj

> ⚠️ **Breaking change** Starting MEDYAN v5.1.0, brancher output is similar to other linkers, where two 3D coordinates (on mother/daughter filament, respectively) are recorded. Previously, only the starting coordinates (on the mother filament) were recorded.

The snapshot file gives the basic trajectory information of the system. It includes a brief
description for all filaments, cross-linkers, motors, and branching points in the system, as
well as information on the current chemical step. It is produced with the following form:

```
chemstepnumber time numfilaments numlinkers nummotors numbranchers
FILAMENT filamentid filamenttype filamentcyllength deltal deltar
beadcoord1x beadcoord1y beadcoord1z beadcoord2x beadcoord2y beadcoord2z ...
...
LINKER linkerid linkertype
startcoordx startcoordy startcoordz endcoordx endcoordy endcoordz
...
MOTOR motorid motortype
startcoordx startcoordy startcoordz endcoordx endcoordy endcoordz
...
BRANCHER brancherid branchertype
startcoordx startcoordy startcoordz endcoordx endcoordy endcoordz
```

## plusend.traj

The plusend file gives the plus end coordinates and types information. The plus end coordinates should be the same as the last bead coordinates in the snapshot.traj for each
filament. The plus end type is recorded as 0, 1, 2, etc. that follows the same order as the
SPECIESPLUSEND in chemistry input files. It is produced with the following form:

```
chemstepnumber time numfilaments numlinkers nummotors numbranchers
F filamentid filamenttype filamentcyllength deltal deltar
plusendcoordx plusendcoordx plusendcoordx
PLUSEND: type
```

##  forces.traj, stresses.traj, and birthtimes.traj

The forces file gives the forces on each element in the system, in similar form to the snapshot file. It is produced with the following format:

```
chemstepnumber time numfilaments numlinkers nummotors numbranchers
F filamentid filamenttype filamentcyllength deltal deltar
bead1property bead2property ...
...
L linkerid linkertype
linkerproperty
...
M motorid motortype
motorproperty
...
B brancherid branchertype
*no property printed for branching points*
...
```

where the properties are as follows:
- `forces.traj`: the magnitude forces on each cylinder, as well as the magnitude of stretching force on each cross-linker and motor are printed.
- `stresses.traj`: the stretching stress on cylinders, cross-linkers, and motors are printed.
- `birthtimes.traj`: the birth time of on cylinders, cross-linkers, and motors are printed.

##  chemistry.traj

The chemistry trajectory file gives the copy numbers of all species in the system, along
with the current chemical step and time. It is produced with the following form:

```
chemstepnumber time
SPECIESNAME COPYNUMBER
```

where `SPECIESNAME` represents the name of the system species and `COPYNUMBER` is the
current copy number of that species at the given timestep.

## concentration.traj

The concentration trajectory file gives the center point coordinates of compartments and
the copy numbers of all diffusing species in the compartment. It is produced with the following form:

```
chemstepnumber time
COMPARTMENT: coordx coordy coordz
SPECIESNAME COPYNUMBER
```

## monomers.traj

The monomers trajectory files gives the number of reactions occurred since last snapshot.
DeltaMinusEnd and DeltaPlusEnd shows the number of cylinder is created and destructed. (Dd)Poly refers to (de)polymerization. IfNucleation = 1 suggests that this filament
is nucleated by nucleation reaction during this period. It is produced with the following
form:

```
chemstepnumber time numfilaments numlinkers nummotors numbranchers
F filamentid filamenttype filamentcyllength DeltaMinusEnd DeltaPlusEnd
DeltaMinusEnd DeltaPlusEnd PolyMinusEnd PolyPlusEnd DepolyMinusEnd DepolyPlusEnd
IfNucleation TotalNumMonomers
```

## dissipation.traj

The dissipation file gives the cumulative changes in the Gibbs free energy of the system
resulting from chemical reactions and mechanical rearrangements. The difference between
the values at consecutive times will approximate the dissipation rates. The distinction
between `chemdiss` and `chemenergy` and between `mechdiss` and `mechenergy` is explained
in accompanying material. The format of the output file is:

```
chemstepnumber time
total chemdiss mechdiss chemenergy mechenergy
```

## HRCD.traj

The high resolution chemical dissipation file gives the cumulative changes in the Gibbs free
energy of the system resulting from chemical reactions, with the contributions from each
reaction specified separately. The order of the reactions is preserved from time step to
time step and is set by the order of their first occurrence in the trajectory. For the change
in Gibbs free energy resulting from diffusion of a diffusing species, the `HRCDDID` is given
as `DIF_SPECIESNAME`. For the change in Gibbs free energy resulting from the unbinding of
linkers or motors, the `HRCDDID` is given as `HRCDIDoff`, where `HRCDID` is that of the corresponding binding reaction. The format of the output file is:

```
chemstepnumber time
HRCDID1 HRCDID2 ...
chemenergy1 chemenergy2 ...
```

Here the `chemenergy` fields are cumulative changes in Gibbs free energy owing to this
reaction.

## HRMD.traj

The high resolution mechanical dissipation file gives the cumulative values of ∆G<sub>mech</sub> and
∆G<sub>mech, diss</sub>, with contributions from each force field specified separately. The format of
the output file is:

```
chemstepnumber time
ForceField1 ForceField2 ...
mechenergy1 mechenergy2 ...
mechdiss1 mechdiss2 ...
```

Here the `mechenergy1` fields are cumulative net changes in mechanical energy owing to
force field 1, and the mechdiss1 are cumulative changes in mechanical energy during energy
minimization owing to force field 1. The difference between these two quantities is explained
in accompanying material. Summing across the rows of the `mechenergy` and `mechdiss` lines
will give the corresponding values found at that time point in the `dissipation.traj` file.
When parsing this file, note that the `Excluded Volume` force field consists of two words
whereas the other force fields (e.g. `Bubble`) consist of only one word.

## CMGraph.traj

The connectivity-based mapping output gives information which can be used to construct
a weighted graph, in which filaments are nodes and the weighted edges between them represent the number of cross-linkers connecting them. The format of the output file is:

```
chemstepnumber time
filid1a filid1b numlinks1 filid2a fildid2b numlinks2 ...
```

Here the `filida` and `filidb` fields are the filament identification numbers, indicating
that this pair of filaments is connected by `numlinks` cross-linkers.

##  motorwalkingevents.traj, linkerbindingevents.traj, linkerunbindingevents.traj

These output files will be generated if the event tracking feature is turned on. They give
detailed information on the spatiotemporal occurrences of motor walking, and cross-linker
binding and unbinding. The format for these output files is:

```
event_t event_x event_y event_z
```

## traj.h5

All desired system information should be stored in the `traj.h5` file. The file has the following structure. Some items are documented inline.

```
🗂️ HDF5.File: traj.h5
├─ 📂 header                             <- contains information about the simulation
│  ├─ 🏷️ version                         <- version of medyan generating this file
│  ├─ 🔢 count                           <- number of snapshot frames
│  ├─ 🔢 finished                        <- whether the simulation finished successfully
│  └─ 📂 meta
│     ├─ 🔢 chem                         <- reconstituded chemistry input file
│     ├─ 🔢 diffusingSpeciesNames
│     ├─ 🔢 energyNames
│     ├─ 🔢 globalFilamentModel
│     ├─ 🔢 globalSpeciesNames           <- names of species reported in each snapshot
│     ├─ 🔢 system                       <- reconstituted system input file
│     ├─ 🔢 vertexColumnNamesFloat64
│     └─ 🔢 vertexColumnNamesInt64
└─ 📂 snapshots                          <- all snapshot data
   ├─ 📂 0                               <- snapshot id starting from 0
   │  ├─ 📂 bubbles
   │  │  ├─ 📂 0
   │  │  │  ├─ 🔢 coords
   │  │  │  ├─ 🔢 id
   │  │  │  ├─ 🔢 radius
   │  │  │  └─ 🔢 type
   │  │  └─ 🔢 count                     <- number of bubbles
   │  ├─ 📂 filaments
   │  │  ├─ 🔢 0                         <- 3xN matrix where N is the number of beads
   │  │  ├─ 🔢 ...
   │  │  └─ 🔢 count                     <- number of filaments
   │  ├─ 📂 linkers
   │  │  ├─ 📂 0
   │  │  │  ├─ 🔢 coords
   │  │  │  ├─ 🔢 id
   │  │  │  ├─ 🔢 subtype                <- integer subtype of linker
   │  │  │  └─ 🔢 type                   <- string of "linker", "motor" or "brancher"
   │  │  └─ 🔢 count                     <- number of linkers
   │  ├─ 📂 membranes
   │  │  ├─ 📂 0
   │  │  │  ├─ 🔢 numBorders
   │  │  │  ├─ 🔢 numTriangles
   │  │  │  ├─ 🔢 numVertices
   │  │  │  ├─ 🔢 packedBorderVertices   <- read "struct OutputStructMembrane" in OutputStruct.hpp for details
   │  │  │  ├─ 🔢 triangleDataInt64
   │  │  │  ├─ 🔢 type
   │  │  │  ├─ 🔢 vertexDataFloat64
   │  │  │  └─ 🔢 vertexDataInt64
   │  │  └─ 🔢 count                     <- number of membranes
   │  ├─ 🔢 diffusingSpeciesCopyNumbers  <- 4D array indexed by [species index, x, y, z]
   │  ├─ 🔢 globalSpeciesCopyNumbers     <- some selected species copy numbers
   │  ├─ 🔢 energies                     <- mechanical energies after minimization
   │  └─ 🔢 time                         <- current time of simulation
   └─ 📂 ...
```
