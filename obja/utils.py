def create_list_edges(faces):
    """Create a list with all the edges reguarding a list of all the faces

    Args:
        faces (np.array): The list of all the faces of the model
    """
    
    # Creation of an empty list to have all the edges
    edges = []
    
    # Enumeration on all the faces
    for (face_index, face) in enumerate(faces):
        
        # Append the first edge
        edges.append((face.a,face.b))
        
        # Append the second edge
        edges.append((face.b,face.c))
        
        # Append the third edge
        edges.append((face.a,face.c))
        
    # Return the list of edges
    return edges




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