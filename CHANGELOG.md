# 5.4.0 (Released 2022-03-27)

## Enhancements
- Added fixed membrane vertex attachments, including initialization and force field. ([#129](https://github.com/medyan-dev/medyan/pull/129))

## Bug fixes
- Fixed the issue where the max force was not updated after recovery operation during conjugate gradient minimization. ([#128](https://github.com/medyan-dev/medyan/pull/128))
- Fixed the memory leak issue during minimization. ([#130](https://github.com/medyan-dev/medyan/pull/130))
- In visualization, fixed the issue where the line visualization was not disabled when the trajectory is disabled (99e6925).


# 5.3.0 (Released 2022-03-14)

## Enhancements
- Membrane
    - Surface protein binding will consume accessible area of a vertex, which affects future binding rates on this vertex. ([#120](https://github.com/medyan-dev/medyan/pull/120))
    - Some integral properties (such as species copy number) on vertices are better redistributed during modification. ([#121](https://github.com/medyan-dev/medyan/pull/121))
    - Re-enabled triangle protect FF, removing border forces. ([#121](https://github.com/medyan-dev/medyan/pull/121))
    - Added another option for curvature computation which is used in Mem3DG. ([#121](https://github.com/medyan-dev/medyan/pull/121))
    - Re-enabled membrane global stretching FF. ([#121](https://github.com/medyan-dev/medyan/pull/121))
    - Added membrane equilibrium volume increase protocol. ([#121](https://github.com/medyan-dev/medyan/pull/121))
    - Added configuration option to mesh adaptation. ([#121](https://github.com/medyan-dev/medyan/pull/121))
    - Enabled optional remeshing during minimization. ([#121](https://github.com/medyan-dev/medyan/pull/121))
    - Added adsorption along with surface diffusion in side routine. ([#121](https://github.com/medyan-dev/medyan/pull/121))
    - Enable more robust border vertex pinning. ([#122](https://github.com/medyan-dev/medyan/pull/122))
- Visualization
    - Added shortcut (default to <kbd>space</kbd>) to toggle play/pause in GUI. ([#120](https://github.com/medyan-dev/medyan/pull/120))
    - In GUI, allows changing the color range and color map of the attribute display. Also, the actual range of the selected membrane attribute will be displayed. ([#124](https://github.com/medyan-dev/medyan/pull/124))
    - Added bubble visualization. ([#126](https://github.com/medyan-dev/medyan/pull/126))
- Others
    - Now the total copy numbers of some selected species are reported in the HDF5 output. ([#121](https://github.com/medyan-dev/medyan/pull/121))
    - Added brief documents on the HDF5 trajectory file. ([#126](https://github.com/medyan-dev/medyan/pull/126))

# Bug fixes
- Update rates right after adsorption or surface diffusion reaction happens. ([#121](https://github.com/medyan-dev/medyan/pull/121))
- Fixed curvature mismatch energy computation and smoothen copy number used in curvature generation using diffusion. ([#121](https://github.com/medyan-dev/medyan/pull/121))
- Fixed rate constant for surface internal reactions. ([#121](https://github.com/medyan-dev/medyan/pull/121))
- Fixed command line `-i` option autofill. ([#121](https://github.com/medyan-dev/medyan/pull/121))


# 5.2.1 (Released 2022-02-10)

## Bug fixes
- Fixed energy curve display on GUI with multiple trajectories. ([#118](https://github.com/medyan-dev/medyan/pull/118))
- Added Boolean data "header/finished" in the h5 trajectory to indicate simulation status. ([#118](https://github.com/medyan-dev/medyan/pull/118))
- Improved NRM heap error report, and fixed heap corruption when infinite propensity is encountered. ([#118](https://github.com/medyan-dev/medyan/pull/118))
- Fixed `CGMethod::maxF` function. Only first `numDof` items will be considered. ([#118](https://github.com/medyan-dev/medyan/pull/118))


# 5.2.0 (Released 2022-02-07)

## Enhancements
- IO
    - Added experimental HDF5 format output, including simulation configuration, element snapshots, energies and diffusing species copy numbers. ([#95](https://github.com/medyan-dev/medyan/pull/95), [#96](https://github.com/medyan-dev/medyan/pull/96), [#100](https://github.com/medyan-dev/medyan/pull/100), [#103](https://github.com/medyan-dev/medyan/pull/103), [#112](https://github.com/medyan-dev/medyan/pull/112), [#117](https://github.com/medyan-dev/medyan/pull/117))
    - While invoking medyan with command line arguments, the input directory will be inferred as the directory of the system input file if `-i` option is not provided. ([#111](https://github.com/medyan-dev/medyan/pull/111))
    - The `config` command can now normalize the input files if `-s` option gives a system input file. ([#111](https://github.com/medyan-dev/medyan/pull/111))
    - s-expression printing now auto indents. ([#111](https://github.com/medyan-dev/medyan/pull/111))
- Mechanics
    - Added a consistency test for volume exclusion between the integral formula and the monomer-based formula. ([#96](https://github.com/medyan-dev/medyan/pull/96))
    - Bubble force fields will not move bubbles that are fixed. ([#107](https://github.com/medyan-dev/medyan/pull/107), [#108](https://github.com/medyan-dev/medyan/pull/108))
    - Add force-induced mechanochemical activation on MTOC and AFM structures. ([#109](https://github.com/medyan-dev/medyan/pull/109), [#110](https://github.com/medyan-dev/medyan/pull/110))
    - Protein curvature mismatch energy at each vertex is now scaled by area fraction instead of molar fraction. ([#115](https://github.com/medyan-dev/medyan/pull/115))
    - Protein curvature mismatch energy is computed on border vertices as well for curvature sensing only. It does not affect curvature generation. ([#115](https://github.com/medyan-dev/medyan/pull/115))
    - Membrane vertex equilibrium area is the same as current area if the membrane is attached to a lipid reservoir. ([#115](https://github.com/medyan-dev/medyan/pull/115))
    - Energy relative change convergence criterion is formally added, with `energy-change-relative-tolerance` key in the input file. ([#115](https://github.com/medyan-dev/medyan/pull/115))
    - Added a special protocol to increase membrane equilibrium area with a constant rate. ([#117](https://github.com/medyan-dev/medyan/pull/117))
    - Membrane remeshing is now placed after minimization ([#117](https://github.com/medyan-dev/medyan/pull/117)), because
        - Membrane-filament shortest distance can be larger after minimization, reducing the chance that some beads go out of the membrane during remeshing.
        - Artifacts on vertex species copy numbers introduced by remeshing can be smoothened by chemical reactions.
- Chemistry
    - Added support for membrane adsorption/desorption involving bulk species. ([#96](https://github.com/medyan-dev/medyan/pull/96))
- GUI
    - Automatic camera adjustment now takes care of z clipping planes as well. ([#96](https://github.com/medyan-dev/medyan/pull/96))
    - Improved formula for camera rotation by mouse. ([#96](https://github.com/medyan-dev/medyan/pull/96))
    - Added energy plots in the GUI. ([#112](https://github.com/medyan-dev/medyan/pull/112))
    - Membranes can be colored with attributes (e.g. protein concentration) in display. ([#114](https://github.com/medyan-dev/medyan/pull/114), [#115](https://github.com/medyan-dev/medyan/pull/115))

## Bug fixes
- Fixed a bug in data dump involving bulk species. ([#96](https://github.com/medyan-dev/medyan/pull/96))
- Fixed an assertion failure issue when the window has zero size. ([#96](https://github.com/medyan-dev/medyan/pull/96))
- Framebuffer size is no longer assumed to be equal to the window size. ([#96](https://github.com/medyan-dev/medyan/pull/96))
- Fixed incorrect free energy of the curvature mismatch model. ([#97](https://github.com/medyan-dev/medyan/pull/97))
- Fixed incorrect number of lipids in curvature mismatch model. ([#100](https://github.com/medyan-dev/medyan/pull/100))
- Fixed memory problem at the end of simulation, arising from membrane reactions incorrectly destructed. ([#100](https://github.com/medyan-dev/medyan/pull/100))
- Fixed incorrect filament ring initialization angle constraint. ([#104](https://github.com/medyan-dev/medyan/pull/104))
- Fixed membrane bending constant not correctly registered after remeshing. ([#111](https://github.com/medyan-dev/medyan/pull/111))
- Fixed membrane geometry not computed before computing energies/forces during force field diagnosis. ([#115](https://github.com/medyan-dev/medyan/pull/115))
- Max distance during minimization recovery applies to vertices as well. ([#115](https://github.com/medyan-dev/medyan/pull/115))
- Fixed parser output for `SPECIALPROTOCOL pin-initial-filament-below-z`. ([#115](https://github.com/medyan-dev/medyan/pull/115))
- Fixed accuracy issue for `toString` for arithmetic types. ([#115](https://github.com/medyan-dev/medyan/pull/115))
- Fixed file dialog problem on Linux using Zenity. ([#115](https://github.com/medyan-dev/medyan/pull/115))
- Membrane surface diffusion also respects the curvature mismatch energy. ([#116](https://github.com/medyan-dev/medyan/pull/116))


# 5.1.0 (Released 2021-12-01)

## Breaking changes
- In chemistry input file, the diffusion coefficient, instead of the diffusion reaction rate (scaled by the size of a cubic compartment), is specified in `SPECIESDIFFUSING`. This enables the fix of incorrect diffusion rate scaling with non-cubic compartments. ([#75](https://github.com/medyan-dev/medyan/pull/75))
- In output file `snapshot.traj`, the brancher is now represented as a linker, where the coordinates on both mother and daughter filaments are recorded. Previously, only coordinates on the mother filament was recorded. ([#79](https://github.com/medyan-dev/medyan/pull/79))

## New features
- Added membrane adsorption/desorption reactions. ([#62](https://github.com/medyan-dev/medyan/pull/62), [#73](https://github.com/medyan-dev/medyan/pull/73), [#88](https://github.com/medyan-dev/medyan/pull/88), [#94](https://github.com/medyan-dev/medyan/pull/94))
- Added an alternative cylinder excluded volume force field. ([#92](https://github.com/medyan-dev/medyan/pull/92))

## Refactoring
- Duration for timed chemistry step is now exact ([#13](https://github.com/medyan-dev/medyan/pull/13), [#18](https://github.com/medyan-dev/medyan/pull/18), [#21](https://github.com/medyan-dev/medyan/pull/21)).
- Largely refactored codes in conjugate gradient method. Specifically, 3 search direction update methods are now grouped into one file. ([#23](https://github.com/medyan-dev/medyan/pull/23), [#27](https://github.com/medyan-dev/medyan/pull/27), [#28](https://github.com/medyan-dev/medyan/pull/28), [#58](https://github.com/medyan-dev/medyan/pull/58), [#59](https://github.com/medyan-dev/medyan/pull/59))
- Reaction/species signals are now implemented using C++ standard library components instead of boost's signals2 library, which provides faster compile speed ([#38](https://github.com/medyan-dev/medyan/pull/38)).
- Different Species are now differentiated using an enum type member `Species::type_` instead of multiple distinct types ([#42](https://github.com/medyan-dev/medyan/pull/42)).
- Optimized function to obtain compartment list from `CompartmentGrid` instance ([#44](https://github.com/medyan-dev/medyan/pull/44)).
- A more secure procedure is used for cylinder information packing (for SIMD line search algorithm). ([#46](https://github.com/medyan-dev/medyan/pull/46))
- Simplified filament initialization and `FilamentData` structure. ([#60](https://github.com/medyan-dev/medyan/pull/60))
- Compartment neighbor information are now index-based instead of pointer-based. ([#66](https://github.com/medyan-dev/medyan/pull/66), [#70](https://github.com/medyan-dev/medyan/pull/70))
- Uses spdlog library for logging. ([#83](https://github.com/medyan-dev/medyan/pull/83))

## Enhancements
- In visualization, enhanced keyboard shortcut and prevented mouse acting simultaneously on GUI and the scene for MEDYAN objects ([#30](https://github.com/medyan-dev/medyan/pull/30)).
- Added simple force field diagnosis upon line search errors, if `try_to_recover_in_line_search_error` is explicitly set to `false` in the input file. ([#34](https://github.com/medyan-dev/medyan/pull/34))
- Added branching point visualization. ([#50](https://github.com/medyan-dev/medyan/pull/50), [#79](https://github.com/medyan-dev/medyan/pull/79))
- Added depth cueing feature in visualization. ([#51](https://github.com/medyan-dev/medyan/pull/51))
- Linker binding on different types of filaments is now supported. ([#78](https://github.com/medyan-dev/medyan/pull/78), [#79](https://github.com/medyan-dev/medyan/pull/79))
- Added automatic camera adjustment in GUI. ([#81](https://github.com/medyan-dev/medyan/pull/81))
- In GUI, using native file selector, the last opened directory will be remembered. ([#81](https://github.com/medyan-dev/medyan/pull/81))

## Bug fixes
- Fixed bugs related to severing ([#15](https://github.com/medyan-dev/medyan/pull/15)).
- Fixed motor unbinding free energy tracking (0a97196).
- Fixed a bug that breaks the restart protocol ([#32](https://github.com/medyan-dev/medyan/pull/32), [#37](https://github.com/medyan-dev/medyan/pull/37)).
- Fixed compiling issue when `FLOAT_PRECISION` is a predefined macro (when `floatingpoint` is `float`) ([#35](https://github.com/medyan-dev/medyan/pull/35)).
- Fixed an issue in parsing string variables during command line parsing ([#36](https://github.com/medyan-dev/medyan/pull/36)).
- Fixed vcpkg creating cache outside repository. ([#48](https://github.com/medyan-dev/medyan/pull/48))
- Fixed infinite loop issue in branching nucleation callback. ([#53](https://github.com/medyan-dev/medyan/pull/53), [#55](https://github.com/medyan-dev/medyan/pull/55))
- Fixed use of freed memory in some chemistry callbacks. ([#57](https://github.com/medyan-dev/medyan/pull/57))
- Fixed undefined behavior and memory problem in hybrid neighbor list when no linker is specified. ([#74](https://github.com/medyan-dev/medyan/pull/74))
- Fixed missing special protocol inputs. ([#89](https://github.com/medyan-dev/medyan/pull/89))
- Fixed filament type parsing issue when dissipation tracking is disabled. ([#93](https://github.com/medyan-dev/medyan/pull/93))


# 5.0.0 (Released 2021-07-13)

## New features
- Added membrane simulation.
- Added visualization and GUI.


# 4.3.0 (Released 2021-07-12)

## New features
- Dropped support for pre C++17 compilers.
- Added simulation configuration generator, and enhanced input file parser to allow structured input using S-Expressions (4d71a27).
- Added `ReactionDy` type that supports reactions with dynamic number of reactants and products (e37feb3).

## Refactoring
- Refactored the data structure in the energy minimization, such that it allows for non-coordinate degrees of freedom (9a02e0f6d).
- Improved reference semantics for `Vec`-like structures as function arguments (27b296ad4).


# 4.2.0 (Released 2021-07-11)

## Enhancements
- Force components that reach >1e15 will trigger an alarm in addition to NaN and Inf values (39ce574).
- Removed thread pool usage (c78fb5e).
- Optimized filament and branching force field calculations (df76443, 4d523e7).
- Added source groups corresponding to the file tree structure in `CMakeLists.txt` (8fc9ead).
- `OPTIMOUT` macro offers more detailed timings of various parts of the code so the user has better understanding of the rate limiting steps in the simulation (873c814).
- Optimized species searching when cloning reactions (52f4c47).
- Optimized addition of dependent reactions (7b86dcd).
- Hessian analysis
    - Eigenvalue computation can be optionally disabled with `EIGENTRACKING: OFF` while computing Hessian matrix (0c455b5).
    - Add output to visualize all eigenmodes in Hessian tracking (16155a6).

## Bug fixes

- Restart
    - During restart phase, motor walking rate was not turned off under a couple of conditions. Fixed that (39ce574).
    - During restart phase, reactions for motor/linker is now turned off (39ce574).
    - During restart phase, `Cylinder::_filID` was not set. Fixed that (106c1e2).
    - Fixed restarted trajectories not having diffusion of chemical species (2903f54).

- Force fields
    - Fixed branching interactions when the offspring filament is attached to the plus end of parent filament (c87d3d9, 840de95).
    - Fixed initial force computation for combined-filament-stretching-and-bending force field, which is no longer enabled by default (99c9bd6).
    - Fixed incorrect forces for branching position cosine (4d523e7).
    - Fixed wrong constant used in branching bending energy computation (a68e859).
    - Fixed incorrect volume exclusion force expressions (49dd9d1).
    - Volume exclusion potential now considers cylinder equilibrium lengths (5d12d11).

- Others
    - After chemistry, when the diffusing species copy numbers are set, now use `up()` and `down()` functions instead of only `setN()` to trigger crosschecks and signals (4b8a5e5).
    - Replaced `std::bind2nd` with lambda function (805b221).
    - Fixed reaction rate scaling by volume in newly created compartments (f6c7783).
    - Fixed the coordinate calculation for binding sites using the `Cylinder::adjustedrelativeposition` function. However, to ensure backward compatibility, it is turned off by default (dbf7527, dbecef5).
    - The cloned reaction is fixed to be non-proto-compartment (e0e6fac).
    - Fixed incorrect filament nucleation when bubbles exist (78a8f8c).
    - Fixed incorrect creation of `FilamentCreationCallback` (7b77123).
    - Fixed build and test workflows on GitHub Actions (bf63f6f).


# 4.1.2 (Released 2020-06-01)

## Enhancements
- New building procedure using `CMake` is supported and recommended (a1b28e254).
- Added a force field that combines filament stretching and bending (772133585).
- Added quadratic line search in gradient descent method (772133585).

## Bug fixes
- The copy number of chemical species are now assigned before dynamic rate initialization (7175987be).
- Fixed branching dihedral force field cosine form (772133585).
- Myosin duty ratio is now calculated at runtime (772133585).

# 4.1.1 (Released 2020-01-30)

## New features
- The system input file no longer requires species number of types specification (b887ba2).
- Rearranged examples and added new ones (48993f8).

## Refactoring and optimizations
- Refactored the logger (a2c69f9).
- Integrated the tests (8de0a0f).
- Increased readability of on-screen outputs.
- `Makefile` default optimization changed from `-Os` to `-O2` (b8468c3).

## Bug fixes
- Fixed distribution generation in chemistry algorithm (5897eed).
- Fixed bugs related to SIMD macros (13fe728).
- Fixed volume exclusion not including short filaments (d0961d4).
- Fixed Myosin motor duty ratio calculation. Now it is based on binding/unbinding rates. (6f57531)

# 4.1.0 (Released 2019-10-29)

## New features
- Added a thread pool implementation, which may facilitate multi-threading computations (fd69e22).
- Added new MTOC functions (e286a3d).
- Added AFM pulling simulation (b581d1a).
- Added mechanical Hessian analysis (b581d1a).
- Added branching dihedral quadratic force field (37b6173).
- Added a cell list data structure for elements contained in the compartments (586f8f5).
- Used a double linked list data structure instead of `std::unordered_set` for `Reactable`s and `Movable`s (0f32b73).
- The dissipation tracking can now have higher resolution, reflecting the mechanical energy change for every force field (5e7eed8).

## Refactoring and optimizations
- Refactored the `Database` class (bc0222c, 3c71316).
- Removed stretched energy computations (ee6220f).
- Various improvements on the restarting procedure (0f32b73).

## Bug fixes
- Fixed motor stretch force not reset before minimization.
- Distance between the boundary and the filaments can be negative now.
- Cylinder neighbor list for volume exclusion will generate multiple neighbor list if there is more than one filament type.
- Filament creation by nucleation and branching is not allowed in partially activated compartment with volume fraction < 0.5. It potentially prevents the infinite while loop during filament creation.
- Fixed `BoundaryCylinderRepulsionIn` force field.
- Fixed `MTOCAttachment` potential.
- Fixed mechanochemical feedback on motor initialization under `PLOSFEEDBACK` version (1fcd9cf).
- Fixed cases where 2 ends a motor binds on the same binding site.
- Fixed compartment transfer/share axis (befaf74).
- Fixed the way of counting number of interactions for filament bending (75bc733).
- Fixed the newly created filament not having mechanochemical feedback (9dc5d27).
- Fixed the problem that the type `floatingpoint` cannot be aliased to `double` (87fad88).
- Fixed `dist_avx.h` not compatible with AVX mode (ce314fa).
- Fixed the issue with changing number of binding sites per cylinder in SIMD binding search (9a39874).
- Fixed the boundary pinning force field (49e254b).
- Fixed minor portability issues on different compilers (eb10ca1).
- Fixed ending simulation message not displayed when simulation finishes (4a2f610).
- `PLOSFEEDBACK` is now turned off by default (3ff0837).
- Fixed the documents for MEDYAN 4.0 speed up comparison (3ff0837).

# 4.0 (Released 2019-07-05)

## New features
- Dropped support for pre C++14 compilers.
- Added support for MSVC compilers and added Visual Studio solution file.
- Added cylindrical boundary type.
- Added support for runtime modification of filament polymerization/depolymerization rate.
- Added support for energy dissipation tracking.

## Optimizations
- Used flattened storage for force field computations.
- Improved performance for neighbor list and binding site search. Binding site search now gains SIMD support. (See [file](./docs/Medyan4.0.pdf) for detailed performance benchmark)

## Bug fixes
- Fixed a bug in boundary repulsion potential.
- Fixed numerical errors that might occur in cylinder volume exclusion potential.

# 3.2.1 (Released 2018-08-23)

## Bug fixes
- Rewrote `Makefile` and fixed the incorrect dependency generation. Also added `PLOSFEEDBACK` to the macro list.
- Fixed a typo in the source.
- Fixed some bugs related to mechanochemical feedback when `PLOSFEEDBACK` is defined.

# 3.2 (Released 2018-08-14)

## Bug fixes
- Filament
    - Fixed a bug on filament severing by cofilin.

        Colfilin reactions required certain callback modifications to effectively simulate them without crashing the program. Those changes are included in this version.

    - Load force computation now considers directionality of filaments.

        Previous models of Brownian ratchet feedback in Medyan considered just the distance from boundary. In this version, both the distance and angle are considered. This leads to a more accurate model for brownian ratchet.

    - Fixed a bug on load force clearing.

        In the previous implementations of MEDYAN, brownian ratchet forces were cleared improperly before being overwritten. As a result, the filament polymerization/depolymerization rates were inaccurate. This is especially true in high χ parameter cases.

- Motors and Linkers
    - Fixed a bug on stretch force computation for motors and linkers.
- Restart protocol can now effectively restart networks with shorter filaments compared to the earlier version.
- Other
    - Improved arrangement of main controller procedure.
    - Bug fix on retrieving compartment grid center coordinate. (used rarely in MEDYAN)
    - Reviewed example files to ensure accuracy of parameters mentioned.
    - `MOTORWALKINGFORWARD` string was used instead of `MOTORWALKINGBACKWARD`. This bug only affects simulations with bi-directional motors.
    - Fixed diffusion bug in `moveBoundary` function.

        Previous version of MEDYAN had a bug which resulted in partial activation of diffusion reactions when a new comaprtment is activated. This has been addressed in this version.

## New features
- Simulations can now control chemical reaction volume based on network span if necessary. Please refer to Usage guide for more details.
- Added output files for trajectory of concentration, plus end type / coordinate and chemical reaction counter on filament.
- Added feature to visualize plus ends in trajectories using VMD. Please refer to UsageGuide for more information.
- Added plotting function to the analysis script in `AnalyzeTrajectory.py`.
- Added example input files for different systems.
- Added a nucleation example input files.
- Added treadmilling tracking.

    Simulations can now track treadmilling in each filament by tracking the total number of polymerization, and depolymerization reactions explicitly in plus and minus ends in addition to nucleation reactions during each chemical evolution cycle.
 
- Added macro `DEBUGCONSTANTSEED`.

    It helps simulate trajectories without stochasticity thereby helping in faster debugging/cross comparison of codes. Simulations might be slower in this mode and so it is better to use smaller systems while debugging.

- Added macro `PLOSFEEDBACK`.

    As many mechanochemical models have been used in publications from Papoian lab, this macro ensures that the feedback model is the same as mentioned in PLOS computatinal biology paper.

    Please refer to Model Guide on Mechanochemical feedback for more information.

    Note: macro changes require edition of `Makefile` and so code should be recompiled to effect the updates.
