# Multi-agent Pathfinding with Radius Abstraction and Deletion Solving
In this project, we implemented an abstraction solver for multi-agent pathfinding with Answer Set Programming. The idea is to first simplify the problem setting by abstracting the map and then translating a solution on that abstracted map back into a solution for the original setting.

## Radius abstraction
The idea behind radius abstraction is picking a center node and then collapsing all nodes within a certain radius into it. We stuck to a radius of 1 as higher radii showed poor results for solving. The challenge here is finding optimal centers to abstract the map as much as possible in a single step. The abstraction is repeated until only a single node remains and all in between levels are kept for the solving.
## Deletion Solving
In deletion solving we now take the abstracted map and solve the problem on it. When we now go back down a level to the less abstracted map, we delete all nodes that were not part of the solution on the higher level. This way we can ignore entire parts of the map for the less abstracted levels.
## Issues
1. The usefulness of this approach depends on the map. Maps where agents have to visit all parts will be reconstructed in ful when deabstracting and will therefore not benefit and instead only incurr the overhead cost of abstraction and multi-level solve.
2. This approach does not guarantee an optimal solution. Traversing an abstracted node can take anywhere between 1 and 3 steps on the next higher level and there is no way of knowing this. What might look shorter on the abstracted map can therefore result in a longer path on the full map.