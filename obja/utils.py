
def check_neighbour(edge, edges, collapse):
    v1 = edge[0]
    v2 = edge[1]
    v1_neighbours = []
    v2_neighbours = []
    for e in edges:
        ve_1 = e[0]
        ve_2 = e[1]
        if v1==ve_1:
            v1_neighbours.append(ve_2)
        elif v1==ve_2:
            v1_neighbours.append(ve_1)
        elif v2==ve_1:
            v2_neighbours.append(ve_2)
        elif v2==ve_2:
            v2_neighbours.append(ve_1)
            
    intersect = [v for v in v1_neighbours if v in v2_neighbours]
    
    return len(intersect) <= 2