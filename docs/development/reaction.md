# Chemical reaction structure in MEDYAN

The chemistry diffusion-reaction simulation is implemented with variants of Gillespie's algorithms, which consists of the following parts that work cooperatively.

## Chemical species

TODO: add description

## Chemical reactions

`ReactionBase` is the abstract base class for all chemical reaction classes. It manages the chemical reaction rates and interacts with the chemistry simulation algorithm. Specifically, in the Next Reaction Method (NRM), it manages the reaction dependencies. It also specifies the interface for reactions, such that an implementation of the `ReactionBase` should include

- how to update dependencies
- what to do when the reaction is fired
- what to do when the reaction is activated or passivated
- how to calculate propensity
- what to do when the reaction rate is updated

In practice, the implementation should be able to access information to all reactant and product species.

An example of the implementation is the `Reaction<M,N>` class template, where `M` and `N` are, respectively, the number of reactants and products, which should be resolved at compile time. Another example of the implementation is the `ReactionDy` class where the number of reactants and products can be specified at run time.

Below is a brief introduction of what a `Reaction<M,N>` can do, including its construction and destruction. `ReactionDy` has a similar implementation, so only the differences will be mentioned.

**(Constructor)** The `ReactionBase` constructor will handle the initialization of reaction rate and factors. The `Reaction<M,N>` constructor will store the address of all the associated species, and then register all other activated reactions that have any reactant species showing up in reactant/product species of this reaction as dependents (ie the change of any species in this reaction will affect the propensities of all the dependent reactions). It also records the address of itself in all associated species.

> ℹ️ The constructor by default sets the new reaction to be **passivated**.


**(Destructor)** The `Reaction<M,N>` destructor will unregister itself from all associated species.

> ⚠️ To avoid dangling pointers, the address of each reaction should not be changed during its lifespan.
>
> ⚠️ All the associated species of a reaction should remain valid and have the address unchanged during the reaction's lifespan.

TODO: other functions
