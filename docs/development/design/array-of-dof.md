# Array of degrees of freedom

Used in energy minimization (or integration of equation of motion, or Monte Carlo methods).

Currently, as of MEDYAN v4.1.1, we store all the coordinate data into a 1D array (wrapped in a `VecArray` class template, which mocks a 3 x N matrix using a 1D array with 3N elements). The forces and other auxiliary data are stored in the same way, and we'll use the coordinate array as the example. Beads hold references to the corresponding data in the array. When a bead is deleted, the `Database` class would mark in the 1D coordinate array with deleted indices, which do not affect other bead coordinate data. When a new bead is created, filling holes in the coordinate array will be prioritized than appending at the end. In this way, there's always a possibility that holes exist in the array. However, the energy minimization method expects a contiguous storage of coordinates, which requires us to "rearrange" the data in that 1D array, meaning to change indices of certain coordinate data to fill in all the holes. The 1D array structure is used and maintained throughout the simulation.

However, those taking part in the energy minimization might not necessarily be Cartesian coordinates in $\mathbb{R}^3$. Some examples are: the local 2D coordinates of a protein on the membrane and the parameters used in exponential curve interpolation for filament parametrization. How should we take care of these parameters? Should we pack these parameters together in that 1D array, or should we simply treat them separately? To answer these questions, we should revisit the decisions we've made to store coordinate data inside a 1D array, to see what are the benefits and what are the costs.

## Coordinates stored in 1D array

Theoretical benefits:

1. (Performance) Operations that are core to the minimization algorithm, like moving coordinates according to the forces, are highly vectorized, resulting in higher performance.
1. (Performance) The bead coordinate data can be rearranged in a way that makes data access of *some* of the force fields contiguous. The filament stretching and bending force fields can potentially benefit from it. It is not obvious how more randomized access could benefit from this, such as the linker stretching force field.
1. (Code) It is made clear that the 1D arrays mainly serve the purpose for the energy minimization algorithm. For example, the "descent direction" in the conjugate gradient method has no obvious physical meaning.

Costs:

1. (Code) When a rearrangement of the array happens, all `array_view`-like objects are invalidated, with only the references in `Bead` class updated. So any code referencing coordinate data must obtain the new data from the corresponding Beads. Currently, `Cylinder::updateAllData()` does this.

Ties:

1. Compared to the implementation where coordinates are stored separately in each bead, a random computation using the coordinates of the bead should not have very different performance, because both require some random access on the memory.

It is worth pointing out that the coordinate array, the force arrays and other auxiliary arrays are not all the information required by the energy minimization process. The force field also needs to know the set of *indices* in those arrays to work with, the information given by the network. Intermediate computation results, such as triangle areas and their derivatives on the coordinates, are also needed by the force fields.

## Non-coordinate degrees of freedom

The game changes if we want to incorporate coordinates that are not Cartesian coordinates in $\mathbb{R}^3$. However, we would still want coordinates of a minimalistic set to be stored contiguously in memory. For example, for the coordinate $(x, y, z)$, with the pointer to the $x$ coordinate being `px`, the address of $y$ and $z$ should still be `px + 1` and `px + 2`.

One way is to continue to store everything into the original 1D array, and then all the previous benefits on the performance of the minimization algorithm would still be there. However, the maintenance of the structure would be very hard. Outside the energy minimization, when different elements are dynamically destroyed, the holes left in the array would be of different sizes, depending on the number of degrees of freedom used by the elements, and, as a result, new elements created may not efficiently find the holes that are suitable to fill. For the same reason, rearrangement of this new 1D array would be hard as well. The solution is to switch back to the original implementation in MEDYAN, where the 1D array is only *created* when entering energy minimization, by the previous "vectorization" process. The array would not be used outside the mechanical processes. In this way, a new cost is introduced: the data copying to the array before energy minimization and from the array after energy minimization. This data copying should not be a bottleneck on the overall performance given that it is a one-time cost per minimization.

Another way would be to store each set of coordinates with the same number of degrees of freedom into a standalone 1D array. For example, the normal coordinates can be stored in the original `VecArray< 3, double >` structure, while 2D coordinates like those used to mark the position on the membrane can be stored in a different `VecArray< 2, double >` structure. In this way, the dynamic element addition/removal works exactly as before, with easy mark-as-deletion and hole-filling processes. The benefit that comes from the highly vectorized operation in energy minimization would be slightly cut down because operations previously performed on a single array now needs to be performed on multiple arrays.

The performance difference with these two ways should not be significantly different, since the cost they introduce is relatively small. From the perspective of writing clearer codes, however, the first way is better at separating purposes: it makes the energy minimization and the rest of the program less coupled, because the coordinate data layout in the memory is not restricted to the layout required by the energy minimization.
