# Predefined macros

A list of all the predefined macros and their usages

| Macro | Description |
|-------|-------------|
| `BOOST_MEM_POOL` | Enable boost memory pool optimizations. |
| `BOOL_POOL_NSIZE` | Set boost memory pool size. |
| `CHECKFORCES_INF_NAN` | Enable checks for `inf` or `NaN` forces. |
| `FLOAT_PRECISION` | If defined, `float` will be used in most places, instead of `double`. |
| `HYBRID_NLSTENCILLIST` | An optimized neighbor list implementation. Conflicts with `NLORIGINAL` and `SIMDBINDINGSEARCH`. |
| `NLORIGINAL` | The neighbor list implementation similar to MEDYAN v3.2. Conflicts with `HYBRID_NLSTENCILLIST` and `SIMDBINDINGSEARCH`. |
| `SIMDBINDINGSEARCH` | Enable SIMD-based neighbor list and binding site pair search protocol. Conflicts with `NLORIGINAL` and `HYBRID_NLSTENCILLIST`. |
| `TRACK_DEPENDENTS` | Track reaction dependents in system. |
| `TRACK_ZERO_COPY_N` | Passivate reactions with zero copy number. |
| `TRACK_UPPER_COPY_N` | Passivate reactions with big copy number. |
