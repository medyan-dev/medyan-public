# Adaptive surface meshing implementation in MEDYAN

## Goals

The goals are to improve the correctness of numerical simulation of membrane deformations. Remeshing will be applied after energy minimization.

| Goal | Explanation |
|------|-------------|
| Proximity     | The new mesh and the original mesh must approximate the same geometry. |
| Size quality  | The vertices should be denser where high local curvatures are observed. |
| Shape quality | The triangles should be as equilateral as possible. |

## Implementations

### Achieving the goals

The goal for **proximity** is discussed in [<a name="Frey2000"></a>Pascal J. Frey, About surface remeshing (2000)] and [<a name="Frey1998"></a>Pascal J. Frey et al, Geometric surface mesh optimization (1998)]. The remeshing operations must respect the geometic measures.

**Size quality** is pursued in most adaptive mesh papers, as the mesh density should be controlled by the local geometry, typically curvature. In terms of the curvature mesh size adaptation, the idea is equivalent as the smoothness criterion, which requires that the normal vectors of any two neighboring triangles are almost parallel. Size quality is mainly achieved by adding/subtracting nodes from the mesh. Node addition are mainly by edge-splitting, and node subtraction are mainly by edge-collapsing.

An additional goal discussed in [[Frey 1998](#Frey1998)] is the **size gradation control**, which means that the gradient of size quality on the surface should not be too big. This will help improve the shape quality below.

**Triangle shape quality** is required by numerical simulations. Many local approximations render bad results when triangles are in bad shape, aka away from being equilateral. Errors might also arise when, for example, negative Voronoi area around a vertex due to bad neighbor triangle shapes. Point relocation (or relaxation) and edge-flipping are the main methods of achieving this goal.

### Mesh operations

**Relaxation** is discussed in [<a name="Cristini2001"></a>Vittorio Cristini et al, An adaptive mesh algorithm for evolving surfaces: simulations of drop breakup and coalescence (2001)]. The vertices are moved inside their tangent planes responding to forces that try to bring edges to their preferred lengths. The sizes of the edges are precomputed to best achieve the size quality and shape quality, via curvature criteria averaged over local regions.

**Node relocation** discussed in [[Frey 1998](#Frey1998)] and [[Frey 2000](#Frey2000)] serves only to achieve shape quality, since size quality has already been achieved via other means.

**Edge-flipping** is performed to increase the neighbor triangle shape quality. In general, it is only performed given (1) the topology after flipping is feasible, (2) the neighbor triangles are almost coplanar, and (3) the neighbor triangle quality will be improved after edge flipping. It is also mentioned in [[Frey 1998](#Frey1998)] that this operation could also improve geometric quality, but in [[Frey 2000](#Frey2000)], the coplanar criterion preserves geometric approximation.

**Edge-splitting** is performed when new vertices are needed to improve the size quality. In [[Frey 1998](#Frey1998)], the new vertex is introduced in the middle of an edge (that is "too long") and then snapped to the geometric support, while in [[Cristini 2001](#Cristini2001)], edge-splitting do not happen individually, but rather inserts 3 vertices at once on the edges of a triangle, equivalent to 3 edge-splittings plus 1 edge-flipping, followed by local relaxation. Local relaxation/edge-flipping might follow each edge-flipping process.

**Edge-collapsing** is performed when vertices should be subtracted to improve the size quality. It is generally achieved by collapsing edges that are "too short". This operation will not be applied if the quality of the neighboring triangles decrease too much. Local relaxation might follow in [[Cristnin 2001](#Cristini2001)].

### Important value calculation

#### Vertex normals

Vertex normals could be computed as a weighted average of neighbor triangle normal vectors. Here we use angles of the vertex in the triangles as the weights, and the resulting vertex normal is effectively the so-called pseudo normal.

#### Curvatures and size criteria

Curvatures can be calculated in a variety of ways, and the size dependency on the curvature can also be different. The easiest way is described in [[Frey 1998](#Frey1998)] where only the neighbor edge direction and triangle normals are used. The curvature information is used to determine the preferred sizes of the edges.

[[Frey 1998](#Frey1998)] and [[Frey 2000](#Frey2000)] discusses rectification of the preferred sizes to control mesh gradation using *H-correction*, while in [[Cristini 2001](#Cristini2001)] the local averaging scheme achieves a similar goal.
