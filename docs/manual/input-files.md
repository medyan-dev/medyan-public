# Input files

The system file is a simple text file that defines all parameters of the simulation. The
MEDYAN executable must take in a system file as a command line argument.
The parameters are defined in a s-expressions:
```lisp
(parameter          parameter-value)
(parameter-group
    (property-1     property-1-value)
    (property-2     property-2-value))
```

The input files can also be generated using MEDYAN's interactive configuration by running `medyan config`, which provides limited configuration capabilities.

All physical quantities in the input files will use the following base units, unless otherwise specified.

| name      | unit |
|-----------|------|
| time      | s    |
| length    | nm   |
| mass      | g    |

Some common derived units are displayed below.

| name      | unit |
|-----------|------|
| force     | pN   |
| energy    | pN⋅nm |
| diffusion coefficient    | nm²/s |

## System input files

### Geometry

The following geometric parameters can be set. All geometry parameters must be set in the system file, or a startup error will result.

| item | type | description |
|------|------|-------------|
| NX | int | Number of compartments in X direction. |
| NY | int | Number of compartments in Y direction. |
| NZ | int | Number of compartments in Z direction. |
| COMPARTMENTSIZEX | double | Size of compartment in X direction. |
| COMPARTMENTSIZEY | double | Size of compartment in Y direction. |
| COMPARTMENTSIZEZ | double | Size of compartment in Z direction. |
| MONOMERSIZE | double | Size of monomer for filament growth . |
| CYLINDERSIZE | double | Size of cylinder in filament. |
| BOUNDARYSHAPE | {SPHERICAL, CUBIC, CAPSULE} | Boundary shape. |
| BOUNDARYDIAMETER | double | Diameter for applicable shapes, including SPHERICAL and CAPSULE geometries. |

The CUBIC BOUNDARYSHAPE creates boundary planes 25nm in from the faces of compartment grid.

If movement of boundaries is desired, the following parameters can also be set. If these parameters are not set, the system will assume non-moving boundaries. Currently, moving boundaries are only implemented for the CUBIC boundary shape.

| item | type | description |
|------|------|-------------|
| BOUNDARYMOVE | {NONE, ALL, TOP} | Movement of a boundary. ALL specifies that all boundaries will move in the given direction, and top specifies that the top of the boundary in the z direction will move. |
| BMOVESPEED | double | Speed of boundary movement in nm/s. If a negative value is given, the boundary will move towards the center of the grid. If positive, the boundary will move away from the center of the grid. |
| BMOVESTARTTIME | double | Time at which the boundary will begin to move. If not specified, the boundary will start moving at the beginning of the simulation. |
| BMOVEENDTIME | double | Time at which the boundary will stop movement. |

### Mechanics

The following mechanical parameters can be set. It is noted that the number of parameters for each force field must match the number of species of that type, specified in the system input file. This must be consistent for all simulation elements, including filaments, cross-linkers, motors, branchers, and bubbles. To set multiple parameters corresponding to multiple species, list the parameter values with space in between after the parameter qualifier.
If a force field type is left blank, that force field will not be included in the simulation.

| item | type | description |
|------|------|-------------|
| FSTRETCHINGTYPE | {HARMONIC} | Filament stretching force field. |
| FSTRETCHINGK | double | Filament stretching force constant. |
| FBENDINGTYPE | {HARMONIC, COSINE} | Filament bending force field. |
| FBENDINGK | double | Filament bending force constant. |
| FBENDINGTHETA | double | Filament bending angle (radians). |
| LSTRETCHINGTYPE | {HARMONIC} | Cross-linker stretching force field. |
| LSTRETCHINGK | double | Cross-linker stretching force constant. |
| MSTRETCHINGTYPE | {HARMONIC} | Motor stretching force field. |
| MSTRETCHINGK | double | Motor stretching force constant. |
| BRSTRETCHINGTYPE | {HARMONIC} | Branching point stretching force field. |
| BRSTRETCHINGK | double | Branching point stretching force constant. |
| BRBENDINGTYPE | {COSINE} | Branching point bending force field. |
| BRBENDINGK | double | Branching point bending force constant. |
| BRBENDINGTHETA | double | Branching point bending angle (radians). |
| BRDIHEDRALFFTYPE | {COSINE} | Branching point dihedral force field. |
| BRDIHEDRALK | double | Branching point stretching force constant. |
| BRPOSITIONTYPE | {HARMONIC} | Branching point position force field. |
| BRPOSITIONK | double | Branching point position force constant. |
| VOLUMEFFTYPE | {integral, monomer} | Volume force type. When monomer-based volume exclusion is used, `volume-exclusion-monomer-interval` can be specified as well. `REPULSION` is the old option for `integral`, but its use is deprecated. |
| VOLUMECUTOFF | double | Volume interaction cutoff distance. |
| VOLUMEK | double | Volume force constant. |
| volume-exclusion-monomer-interval | list int | Interval of monomer sampling for volume exclusion for each filament type. |
| BOUNDARYFFTYPE | {REPULSIONEXP} | Boundary force type. |
| BOUNDARYCUTOFF | double | Boundary interaction cutoff distance. |
| BOUNDARYINTERACTIONK | double | Boundary force constant. |
| BOUNDARYSCREENLENGTH | double | Boundary screening length constant. |
| BUBBLEFFTYPE | {REPULSIONEXP} | Bubble force type. |
| BUBBLECUTOFF | double | Boundary interaction cutoff distance. |
| BUBBLEINTERACTIONK | double | Bubble force constant. |
| BUBBLESCREENLENGTH | double | Bubble screening length constant. |
| BUBBLERADIUS | double | Bubble radius. |
| NUMBUBBLETYPES | int | Number of different bubble types. |
| MTOCFFTYPE | {ATTACHMENTHARMONIC} | MTOC force type. |
| membrane-tension-ff-type | {CONSTANT} | Membrane tension type. |
| membrane-bending-ff-type | {HELFRICH, HELFRICH_QUADRATIC} | Membrane bending type. In quadratic mode, the spontaneous curvature is always assumed to be zero. |
| volume-conservation-ff-type | {MEMBRANE} | Volume conservation type. |
| triangle-bead-volume-ff-type | {REPULSION} | Triangle bead volume exclusion force type. |
| triangle-bead-volume-k | float | Triangle bead volume exclusion force constant. |
| triangle-bead-volume-cutoff | float | Triangle bead volume exclusion cutoff distance. |
| triangle-bead-volume-cutoff-mech | float | Triangle bead volume exclusion cutoff distance during mechanical minimization. |

The system mechanical energy is minimized using the minimization algorithm, whose parameters can be specified as follows.

| item | type | description |
|------|------|-------------|
| CONJUGATEGRADIENT | {POLAKRIBIERE, FLETCHERRIEVES, STEEPESTDESCENT} | Type of conjugate gradient minimization. |
| GRADIENTTOLERANCE | double | Gradient tolerance in conjugate gradient (in pN). |
| MAXDISTANCE | double | Maximum distance beads can be moved in minimization. |
| LAMBDAMAX | double | Maximum lambda that can be returned in line search. |
| try-to-recover-in-line-search-error | {false, true} | Defaults to true. If set to false, whenever line search fails to find a lower energy, the program will terminate with a diagnostic message. |

### Chemistry

The following chemical parameters can be set. It should be noted that the number of parameters listed for each chemical species type that resides on a filament must match the number of filament types, specified in the system input file. This must be consistent for all filament types. To set multiple parameters corresponding to multiple filaments, list the parameters with space in between after the parameter qualifier.

All chemical parameters must be set unless otherwise noted in the description. For the motor parameters, the number of parameters must match the number of motor species in the system. For more information on chemical algorithms, see [Popov et al (2016)](https://doi.org/10.1371/journal.pcbi.1004877).

An alternate set of parameters can be specified in replacement of `RUNTIME` for smaller systems in which simulation time is based on explicit reaction steps; if `RUNTIME` is not initialized or set to zero, the parameter `RUNSTEPS` and its associated chemical step-based parameter set will be used if provided.

| item | type | description |
|------|------|-------------|
| CHEMISTRYFILE | string | Input chemistry file. Should be in the input directory. |
| CALGORITHM | {GILLESPIE, NRM} | Chemistry algorithm used. |
| RUNSTEPS | int | Number of total chemical steps. If `RUNTIME` is set, will not be used. |
| RUNTIME | double | Total runtime of simulation. |
| SNAPSHOTSTEPS | int | Number of steps per snapshot. If `SNAPSHOTTIME` is set, will not be used. |
| SNAPSHOTTIME | double | Time of each snapshot. |
| MINIMIZATIONSTEPS | int | Number of chemical steps per mechanical equilibration. If `MINIMIZATIONTIME` is set, will not be used. |
| MINIMIZATIONTIME | double | Time between each mechanical equilibration. |
| NEIGHBORLISTSTEPS | int | Number of chemical steps per neighbor list update. This includes updating chemical reactions as well as force fields which rely on neighbor lists. If `NEIGHBORLISTTIME` is set, will not be used. |
| NEIGHBORLISTTIME | double | Time between each neighbor list update. |
| INITIALSLOWDOWNTIME | double | Length of time at the beginning of the simulation to run mechanical equilibrations and neighbor list updates 10x more frequently. Disabled by default. |
| NUMFILAMENTTYPES | int | Number of different filament types. |
| NUMBINDINGSITES | int | Number of binding sites per cylinder for each filament type defined. This will set binding sites for cross-linkers, motors, and other binding molecules. |
| NUMMOTORHEADSMIN | int | Minimum number of motor heads per motor species defined. |
| NUMMOTORHEADSMAX | int | Maximum number of motor heads per motor species defined. |
| MOTORSTEPSIZE | double | Single motor head step size. |
| DISSIPATIONTRACKING | {OFF, ON} | Whether to switch on the dissipation tracking feature. |
| LINKERBINDINGSKIP | int | Switches on the different binding tracking feature to allow motors to have more binding spots per cylinder than linkers. The specified integer is the number of binding sites that the cross-linkers will skip before accepting a possible binding site. |
| allow-same-filament-pair-binding | bool | Whether pairwise bindings on the same filament is allowed. Even if this is turned off, pairwise bindings will not happen on same or neighboring cylinders. |
| EVENTTRACKING | {OFF, ON} | Whether to switch on the event tracking feature. |
       
### Dynamic rates

The following dynamic rate forms and parameters can be set. These parameters are characteristic lengths and amplitudes of the rate changing equations outlined in [Popov et al (2016)](https://doi.org/10.1371/journal.pcbi.1004877). These can be tuned to mimic the stall and unbinding mechanochemical coupling of cross-linkers and myosin II motors. Note that if dynamic rates are enabled, the number of dynamic rate forms for each type of reaction must match the number of species of that type specified in the system input file, i.e. the number of forms for cross-linker unbinding must match the number of cross-linker species, etc.

The number of parameters specified for each type of dynamic rate form must match the number of parameters required for those forms. See below for details, and see [Popov et al (2016)](https://doi.org/10.1371/journal.pcbi.1004877) for more information on the explicit forms. Parameters must be listed in order of the form that they correspond to, also corresponding to the species that they represent.

| item | type | description |
|------|------|-------------|
| DFPOLYMERIZATIONTYPE | {BROWRATCHET} | Filament polymerization dynamic rate form. |
| DFPOLYMERIZATIONLEN | double | Characteristic length for filament polymerization dynamic rate form. |
| DLUNBINDINGTYPE | {CATCHSLIP, SLIP} | Cross-linker unbinding dynamic rate form. If `CATCHSLIP`, two parameters for `DLUNBINDINGLEN` and `DLUNBINDINGAMP` are needed to define the functional form. If `SLIP`, one `DLUNBIDINGLEN` is needed to define the functional form. |
| DLUNBINDINGLEN | double | Characteristic length of cross-linker unbinding dynamic rate form. |
| DLUNBINDINGAMP | double | Amplitude of cross-linker unbinding dynamic rate form. |
| DMUNBINDINGTYPE | {LOWDUTYCATCHSLIP, LOWDUTYSLIP} | Myosin II unbinding dynamic rate form. If `LOWDUTYCATCHSLIP`, two parameters for `DMUNBINDINGFORCE` are needed to define the functional form. If `LOWDUTYSLIP`, one `DMUNBIDINGFORCE` is needed to define the functional form. |
| DMUNBINDINGFORCE | double | Characteristic force of myosin II unbinding dynamic rate form. |
| DMWALKINGTYPE | {LOWDUTYSTALL} | Myosin II walking dynamic rate form. | 

### Membrane profile and initialization

A membrane profile can be defined using the following syntax:
```lisp
(membrane <profile-name>
    (<property> <value>)
    ...)
```
where membrane properties include the following parameters.

| item | type | description |
|------|------|-------------|
| vertex-system | {material, general} | In material vertex system, each vertex represents a patch of membrane with a fixed number of lipid molecules. In general vertex system, a vertex simply represents a point on the membrane surface. |
| area-k | float | Area elasticity of membrane. Unit pN/nm. |
| bending-k | float | Bending elasticity of membrane. Unit pN⋅nm. |
| eq-curv | float | Spontaneous curvature of membrane. Unit 1/nm. |
| tension | float | Membrane tension. Unit pN/nm. |
| volume-k | float | Volume conservation force constant of a enclosing membrane. Unit pN/nm². |

Membrane can be initialized with a specified membrane profile, using the following properties:
```lisp
(init-membrane <profile-name>
    (<property> <value>)
    ...)
```
If the membrane profile name was not defined in the input file, a startup error will occur.
The membrane initialization properties are defined using the following parameters.

- `mesh`: A list describing the initial membrane shape. Currently supporting the following shapes:
    - An ellipsoid whose principal axes are parallel with the x, y, and z axes. Usage: `ELLIPSOID center-x center-y center-z radius-x radius-y radius-z`.
    - A plane specified by a point and a normal vector. A bounding box is also needed to specify the sampling range. Usage: `PLANE center_xyz... normal_xyz... box_origin_xyz... box_size_xyz...`.
- `eq-area-factor`: A floating point value, such that the equilibrium area is the initial area multiplied by this factor.


### Starting filament configuration

These parameters define the initial configuration and length of filaments in the system. It is noted that at least one filament, plus end, and minus end chemical species must be initialized in the chemistry input file, or a startup error will result.

| item | type | description |
|------|------|-------------|
| FILAMENTFILE | string | Name of filament initialization file. This is not required. |
| NUMFILAMENTS | int | Number of random filaments to initialize. These filaments will be randomly distributed in the system volume. |
| FILAMENTLENGTH | int | Number of cylinders per filament to initialize, defining the initial length of the filaments. |
| FILAMENTTYTPE | int | Filament type to initialize. |
| PROJECTIONTYPE | {STRAIGHT, ZIGZAG, ARC, PREDEFINED} | Specifies how the beads are sampled between two ends of a filament. |

Projection type meaning for a filament specified by a set of 3D Cartesian coordinates `[v0, v1, v2 ...]`, and the number of beads.

- `STRAIGHT` - Creates a filament with minus end at `v0`, and extends number-of-bead full-size cylinders in `v0 -> v1` direction. `v2, v3 ...` are ignored.
- `ZIGZAG` - Creates a filament with minus end at `v0`, and extends number-of-bead full-size cylinders in (1) `v0 -> v1` direction (2) another different direction alternatively. `v2, v3 ...` are ignored.
- `ARC` - Not sure. (TODO: NEED DOCS)
- `PREDEFINED` - Creates a filament with bead coordinates `[v0, v1, v2 ...]`. WARNING: Each cylinder in the filament is treated as a full-sized cylinder, no matter what the initial bead coordinates are. That means each cylinder in the filament can be compressed or stretched initially.

### Starting bubble configuration

The following bubble initialization parameters can be set. These parameters define the initial configuration of bubbles in the system, similar to the filament configuration parameters. It is noted that at least one type of bubble must be set, or a startup error will result.

| item | type | description |
|------|------|-------------|
| BUBBLEFILE | string | Name of bubble initialization file. This is not required. |
| NUMBUBBLES | int | Number of random filaments to initialize. These filaments will be randomly distributed in the system volume. |
| BUBBLETYTPE | int | Bubble type to initialize. |

The following syntax is used to initialize a Microtubule Organizing Center (MTOC), or a bead for Atomic Force Microscopy (AFM), which are both implemented as a bubble with extra parameters.
```lisp
(init-mtoc
    (<property> <value>...)
    ...)
(init-afm
    (<property> <value>...)
    ...)
```

where most properties are shared by both MTOC and AFM. The properties are listed below.

| item | type | description |
|------|------|-------------|
| bubble-type | int | Type of bubble to initialize. |
| bubble-coord | list float | Coordinates of the bubble center. |
| bubble-fixed | {false, true} | If the bubble is fixed, it's coordinates will not change during energy minimization. |
| filament-type | int | Type of filament attachment. |
| num-filaments | int | Number of filaments to attach to the bubble. |
| num-cylinders-per-filament | int | Number of cylinders per filament to attach to the bubble. |
| theta1, theta2, phi1, phi2 | float | Restricts the initial orientation of the filaments under certain transformations (read source code to see the details). Default to (0, 1, 0, 1), which allows all possible orientations. |
| attachment-stretching-k | float | Stretching force constant for filament attachments. |

### Special protocols

The following special protocols can be initialized. These protocols must be set on different lines, so users should specify a new parameter, on separate lines, for each setup desired.

```lisp
(SPECIALPROTOCOL <name> <parameters>...)
```

| name | parameters | description |
|------|------------|-------------|
| PINBOUNDARYFILAMENTS | `<pinK> <pinDistance> <pinTime>` | Tether minus and plus ends that are within `pinDistance` (nm) from the boundary after `pinTime` (s). This will result in additional forces on the actin network form the boundary. |
| PINLOWERBOUNDARYFILAMENTS | `<pinK> <pinTime> <pinFraction>` | Tether minus and plus ends that are within `pinDistance` (nm) from the lower boundary after `pinTime` (s). `pinDistance` has a default value (250 as of v5.1.0), but can be overwritten by other pinning protocols. |
| pin-initial-filament-below-z | `<pinK> <pinZ>` | Pin all initial beads with z coordinate lower than `pinZ` (nm). |
| MAKEFILAMENTSSTATIC, MAKELINKERSSTATIC | `<time>` | Make either filament or cross-linker chemistry static after a certain amount of `time`. |
| RATEDEPEND | `<time> <force>` | Starting at `time`, increase plus end polymerization rate for actin filaments under larger tension than `force` (pN). |
| AFM | `<step1> <step2> <iter-change> <step-total> <step-time>` | AFM protocol. |
| scale-membrane-eq-area | `<rate> <min-eq-area>` | For all membranes without lipid reservoir, increase its equilibrium area with `rate` (nm^2/s). Each equilibrium area cannot drop below `min-eq-area` (nm^2). |
| scale-membrane-eq-volume | `<rate> <min-eq-volume>` | For all closed membranes, increase its equilibrium volume with `rate` (nm^3/s). Each equilibrium volume cannot drop below `min-eq-volume` (nm^3). |


## Chemistry input files

The chemistry input file, whose name is specified in the system input file, contains the chemical configuration of the system, including species and reactions. It is noted that the order in which cross-linker, motor, and branches species are defined in the chemistry input file should match the relevant mechanical parameters, which are defined in the system input file. The number of species of each type should also match the SystemFile’s species type numbers, or a startup error will result. All species names given must be unique strings, or a startup error will result. In all species and reaction definitions, `FILAMENTTYPE` is an integer that specifies the type of filament that this filament species belongs to. For example, if there are two filament types defined, the `FILAMENTTYPE` parameter could be 0 or 1. An invalid value of this parameter will result in an error.

### Species

Different types of species can be defined as follows:

- A diffusing species is defined in the following form:

    > ⚠️ **Breaking change** starting MEDYAN v5.1.0, `<DIFFCOEFF>` means the 3D diffusion coefficient with dimension nm<sup>2</sup>/s. Previously, it meant the diffusion reaction rate between compartments with dimension s<sup>-1</sup>, obtained from diffusion coefficient and the size of a cubic compartment. For example, if 500 nm compartments were used and the diffusion reaction rate was "1.0", it should be changed to "0.25E6".

        SPECIESDIFFUSING <NAME> <COPYNUMBER> <DIFFCOEFF> <RELEASETIME> <REMOVALTIME> <QUALIFIER> (<NUMEVENTS>)

    where `NAME` is any string defining the name of the species, `COPYNUMBER` is the number of molecules of that species in the system, and `DIFFCOEFF` is a float value that determines the diffusion coefficient of this molecule in the solution. `RELEASETIME` specifies when this molecule populates the system in simulation (in seconds). `REMOVALTIME` specifies whether the species should be removed from the simulation. If no removal is desired, this can be set to 0.

    The `QUALIFIER` field is used to define the type of reacting species. The options are the following:

    - `REG` : A regular reacting species. Copy numbers are updated typically.
    - `AVG` : An averaging reacting species. The species will use a copy number averaged over a set number of copy number changes (`NUMEVENTS`) for efficiency.

    The `NUMEVENTS` field, denoted in parentheses as optional, only used in the case of defining an averaging reacting species. If using a regular, this should not be included in the file or an error will result.

- A bulk species, which is assumed to be spatially homogeneous, is defined in the
following form:

        SPECIESBULK <NAME> <COPYNUMBER> <RELEASETIME> <REMOVALTIME> <QUALIFIER>

    where `NAME` is any string defining the name of the species, `COPYNUMBER` is the number of molecules of that species in the system, and `RELEASETIME` specifies when this molecule populates the system in simulation (in seconds). `REMOVALTIME` specifies whether the species should be removed from the simulation. If no removal is desired, this can be set to 0. The `QUALIFIER` field is used to define the type of reacting species. The options are the following:

    - `REG` : A regular reacting species. Copy numbers are updated typically.
    - `CONST` : An constant reacting species. The species will never change copy number upon reacting.

- Any filament-related species can be defined in the following form:

        SPECIES<SPECIESTYPE> <NAME> <FILAMENTTYPE>

    where `SPECIESTYPE` can be:

    - `FILAMENT` : A filamentous species. At least one filament species must be defined if using filaments in simulation.
    - `PLUSEND` : A plus end species on a filament, which is defined as the front of the filament. There must be at least one plus end species for every filament species defined in the system.
    - `MINUSEND` : A minus end species on a filament, which is defined as the back of the filament. There must be at least one minus end species for every filament species defined in the system.
    - `BOUND` : A bound species on a filament. There must be at least one bound species defined for each filament type.
    - `LINKER` : A cross-linker species. The ordering of cross-linker initializations should match their mechanical parameters, as stated above.
    - `MOTOR` : A myosin II motor species. The ordering of motor initializations should match their mechanical parameters, as stated above.
    - `BRANCHER` : A branching species. The ordering of branches initializations should match their mechanical parameters, as stated above.

### Binding sites

For every species that binds to filaments (linkers, motors, branchers), a binding site species must be set. This binding site must be a bound species on any filament type. It is declared in the following form:

    LINKERBINDINGSITE    <NAME> <FILAMENTTYPE>
    MOTORBINDINGSITE     <NAME> <FILAMENTTYPE>
    BRANCHERBINDINGSITE  <NAME> <FILAMENTTYPE>

where `NAME` is the name of a pre-defined bound species on a filament of type `FILAMENTTYPE`.

### Reactions

Reaction definitions must follow these common rules:

- Species that are defined in reactions must be previously defined in the chemistry file.
- For filament-related reactions, most species type and ordering parameters are fixed; if they are fixed, they will be pre-defined in the reaction definition below. If the ordering is not properly followed, a startup error will result.
- All species declarations in a reaction must be separated by white space, with `+` markers between reactants and products. A `->` must be placed between reactants and products, separated by whitespace. If this syntax is not followed, a startup error will result.
- The optional string `HRCDID` and accompanying float `DELGZERO` specify the identity and the ∆G_0 value for the reaction, respectively, for use in dissipation tracking. If this feature is turned on, then this field must be supplied, and if it is turned off then this field must be omitted. Currently only some reactions support dissipation tracking, as specified below, and it is only supported when the Next Reaction Method algorithm choice is used. For those reactions which do not support dissipation tracking, the `HRCDID` and `DELGZERO` fields should not be set. This allows those reactions to be included in the chemical system while allowing dissipation tracking for supported reactions.

Different types of reactions can be defined as follows:

- A general reaction between any bulk or diffusing species can be defined in the
following form:

        (GENREACTION
            [<DELGZERO>:<HRCDID>]
            <NAME>:BULK/DIFFUSING + <NAME>:BULK/DIFFUSING + ...
                -> <NAME>:BULK/DIFFUSING + <NAME>:BULK/DIFFUSING + ...
            <RATE>)

    where any bulk or diffusing species can be included, and `RATE` is a float value that determines the rate constant of the reaction.
    
    This reaction supports dissipation tracking, so if the feature is turned on, then `HRCDID` should be set to a user specified short unique string, and `DELGZERO` should be set to a float value based on the user’s parameterization of the chemical energetics.

- A bulk reaction between bulk species only can be defined in the following form:

        BULKREACTION <NAME>:BULK + <NAME>:BULK + ... -> <NAME>:BULK + <NAME>:BULK + ... <RATE>

    where any bulk species can be included. If the reaction only contains bulk species, it must be specified as a bulk reaction. `RATE` is a float value that determines the rate constant of the reaction.
    
    This reaction does not support dissipation tracking, so `HRCDID` and `DELGZERO` should not be provided.

- A polymerization reaction can be defined in the following form:

        (POLYMERIZATIONREACTION
            [<DELGZERO>:<HRCDID>] <FILAMENTTYPE>
            <NAME>:BULK/DIFFUSING + <NAME>:PLUSEND/MINUSEND
                -> <NAME>:FILAMENT + <NAME>:PLUSEND/MINUSEND
            <RATE>)

    where `NAME` is the string name of the species, and `RATE` is a float value that determines the rate constant of the reaction. It is noted that the first species listed can be either `DIFFUSING` or `BULK`, and the reaction can contain a `PLUSEND` or `MINUSEND`.

    This reaction will polymerize the filament, producing a new chemical species on the end of the filament and increasing the length of the filament by a single monomer. 

    This reaction supports dissipation tracking, so if the feature is turned on, then `HRCDID` should be set to a user specified short unique string, and `DELGZERO` should be set to a float value based on the user’s parameterization of the chemical energetics.

- A depolymerization reaction can be defined in the following form:

        (DEPOLYMERIZATIONREACTION
            [<DELGZERO>:<HRCDID>] <FILAMENTTYPE>
            <NAME>:FILAMENT + <NAME>:PLUSEND/MINUSEND
                -> <NAME>:BULK/DIFFUSING + <NAME>:PLUSEND/MINUSEND
            <RATE>)

    where `NAME` is the string name of the species, and `RATE` is a float value that determines the rate constant of the reaction. It is noted that the third species listed can be either `DIFFUSING` or `BULK`, and the reaction can contain a `PLUSEND` or `MINUSEND`.

    This reaction will depolymerize the filament, removing a chemical species from the end of the filament and decreasing the length of the filament by a single monomer.

    This reaction supports dissipation tracking, so if the feature is turned on, then `HRCDID` should be set to a user specified short unique string, and `DELGZERO` should be set to a float value based on the user’s parameterization of the chemical energetics.

- A cross-linker reaction between two filaments can be defined in the following form:

        (LINKERREACTION
            [<DELGZERO>:<HRCDID>] 0
            <NAME>:BOUND:1 + <NAME>:BOUND:2 + <NAME>:BULK/DIFFUSING
                <-> <NAME>:LINKER:1 + <NAME>:LINKER:2
            <ONRATE> <OFFRATE> <RMIN> <RMAX>)

    where `NAME` is the string name of the species, and `ONRATE` and `OFFRATE` are float values that determines the rate constant of the binding and unbinding reactions. `RMIN` and `RMAX` are the range of the chemical reaction, and this can be set depending on the structure of the simulated cross-linker. It is noted that the third species listed can be either `DIFFUSING` or `BULK`. The bound species listed must be the corresponding cross-linker binding site.

    This reaction produces cross-linker species at two separate positions on each respective filament which are chemically and mechanically connected. If mechanical force fields are defined for the cross-linkers, a potential will be created between the filaments. The unbinding reaction will remove these species from the filaments, as well as remove any linker potentials that have been created between the filaments.

    This reaction supports dissipation tracking, so if the feature is turned on, then `HRCDID` should be set to a user specified short unique string, and `DELGZERO` should be set to a float value based on the user’s parameterization of the chemical energetics.

- A motor reaction between two filaments can be defined in the following form:

        (MOTORREACTION
            [<DELGZERO>:<HRCDID>] 0
            <NAME>:BOUND:1 + <NAME>:BOUND:2 + <NAME>:BULK/DIFFUSING
                <-> <NAME>:MOTOR:1 + <NAME>:MOTOR:2
            <ONRATE> <OFFRATE> <RMIN> <RMAX>)

    where `NAME` is the string name of the species, and `ONRATE` and `OFFRATE` are float values that determines the rate constant of the binding and unbinding reactions. `RMIN` and `RMAX` are the range of the chemical reaction, and this can be set depending on the structure of the simulated motor. It is noted that the third species listed can be either `DIFFUSING` or `BULK`. The bound species listed must be the corresponding motor binding site.

    This binding reaction produces motor species at two separate positions on each respective filament which are chemically and mechanically connected. If mechanical force fields are defined for the motor, a potential will be created between the filaments. The unbinding reaction will remove these species from the filaments, as well as remove any motor potentials that have been created between the filaments.

    This reaction supports dissipation tracking, so if the feature is turned on, then `HRCDID` should be set to a user specified short unique string, and `DELGZERO` should be set to a float value based on the user’s parameterization of the chemical energetics.

- A motor walking reaction can be defined in the following form:

        (MOTORWALKINGREACTION
            [<DELGZERO>:<HRCDID>] <FILAMENTTYPE>
            <NAME>:MOTOR:N/N+1 + <NAME>:BOUND:N/N+1
                -> <NAME>:MOTOR:N/N+1 + <NAME>:BOUND:N/N+1
            <RATE>)

    where `NAME` is the string name of the species, and `RATE` is a float value that determines the rate constant of the reaction. The choice of `N`/`N+1` will determine whether the motor is stepping forward or backward. A motor movement from `N` to `N+1` is defined as forward movement (towards the plus end of the filament), and the opposite is backward (towards the minus end). These choices for the reactants and products must be self-consistent as well as consistent with the bound species positions chosen in the reaction, or a startup error will result. The bound species listed must be the corresponding motor binding site.

    This reaction will move a motor head in the given direction.

    This reaction supports dissipation tracking, so if the feature is turned on, then `HRCDID` should be set to a user specified short unique string, and `DELGZERO` should be set to a float value based on the user’s parameterization of the chemical energetics.

- A branching reaction can be defined in the following form:

        (BRANCHINGREACTION
            <FILAMENTTYPE>
            <NAME>:BULK/DIFFUSING + <NAME>:BULK/DIFFUSING + <NAME>:BOUND
                <-> <NAME>:BRANCHER + <NAME>:PLUSEND
            <ONRATE> <OFFRATE> <NUCLEATIONZONE> <NUCLEATIONDIST>)

    where `NAME` is the string name of the species, and `ONRATE`, `OFFRATE` are float values that determine the rate constants of the reaction. It is noted that the first and second species listed can be either `DIFFUSING` or `BULK`. The bound species listed must be the corresponding branching binding site.

    The `NUCLEATIONZONE` and `NUCLEATIONDIST` specify the volume in which a branching reaction can occur. The choices for the zone parameter are the following

    - `ALL` : A new filament can nucleate anywhere in the simulation volume due to branching.
    - `BOUNDARY` : A new filament can nucleate a given distance away from a boundary due to branching, specified by the `NUCLEATIONDIST` from the system boundary.
    - `TOPBOUNDARY` : Similar to `BOUNDARY` except only in the top half of the volume (in the z direction).

    It is noted that `NUCLEATIONDIST` needs to be specified for all nucleation zones, but it is unused for `ALL`.

    This reaction will create a new branching point, as well as a filament with the desired chemical plus end. If mechanical force fields are defined for the branching point, a potential will be created between the parent and child filament. The unbinding reaction will remove the branching point from the filaments, thus freeing the child filament from the parent. It will also remove any branching point potentials that have been created between the filaments.

    This reaction does not support dissipation tracking, so `HRCDID` and `DELGZERO` should not be provided.

- A nucleation reaction can be defined in the following form:

        (NUCLEATIONREACTION
            <FILAMENTTYPE>
            <NAME>:BULK/DIFFUSING + <NAME>:BULK/DIFFUSING
                -> <NAME>:PLUSEND + <NAME>:FILAMENT + <NAME>:MINUSEND
            <RATE>)

    where `NAME` is the string name of the species, and `RATE` is a float value that determines the rate constant of the reaction. It is noted that the first and second species listed can be either `DIFFUSING` or `BULK`.

    This reaction will create a new filament with the given chemical plus end, minus end, and filament species. PLEASE REFER TO THE EXAMPLE FILES FOR A COMPLETE NUCLEATION CYCLE.

    This reaction does not support dissipation tracking, so `HRCDID` and `DELGZERO` should not be provided.

- A destruction reaction can be defined in the following form:

        (DESTRUCTIONREACTION
            <FILAMENTTYPE>
            <NAME>:PLUSEND + <NAME>:MINUSEND -> <NAME>:BULK/DIFFUSING + <NAME>:BULK/DIFFUSING
            <RATE>)

    where `NAME` is the string name of the species, and `RATE` is a float value that determines the rate constant of the reaction. It is noted that the third and fourth species listed can be either `DIFFUSING` or `BULK`.

    This reaction will destroy a filament, removing it from the system.

    This reaction does not support dissipation tracking, so `HRCDID` and `DELGZERO` should not be provided.

- A filament aging reaction can be defined in the following form:

        (AGINGREACTION
            [<DELGZERO>:<HRCDID>] <FILAMENTTYPE>
            <NAME>:FILAMENT/PLUSEND/MINUSEND -> <NAME>:FILAMENT/PLUSEND/MINUSEND
            <RATE>)

    where `NAME` is the string name of the species, and `RATE` is a float value that determines the rate constant of the reaction. Either of the reactant or product species can be `FILAMENT`, `PLUSEND`, or `MINUEND`, but the product and reactant species must be the same type, or a startup error will result.

    This reaction will change the chemical species that resides in a filament.

    This reaction supports dissipation tracking, so if the feature is turned on, then `HRCDID` should be set to a user specified short unique string, and `DELGZERO` should be set to a float value based on the user’s parameterization of the chemical energetics.

- A filament severing reaction can be defined in the following form:

        SEVERINGREACTION <FILAMENTTYPE> AT <NAME>:FILAMENT <RATE>

    where `NAME` is the string name of the species, and `RATE` is a float value that determines the rate constant of the reaction.

    This reaction will sever the filament at the closest cylinder connection to a given chemical position, producing two child filaments.

    This reaction does not support dissipation tracking, so `HRCDID` and `DELGZERO` should not be provided.
