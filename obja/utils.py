def edg2key(p1:int,p2:int)->str:
    """Create a str key with two points

    Args:
        p1 (int): the first point
        p2 (int): the second point

    Returns:
        str: the final key
    """
    
    # We want the smallest number first
    if p1 < p2:
        return str(p1) + "," + str(p2)
    else:
        return str(p2) + "," + str(p1)
    
    
def key2edg(key: str) -> tuple:
    """Convert a str key back into two points 

    Args:
        key (str): the key in the format 'p1,p2'

    Returns:
        tuple: a tuple of two integers (p1, p2)
    """
    
    # Split the key 
    p1, p2 = map(int, key.split(","))
    
    return (p1, p2)
    


def create_dict_edges(faces):
    """Create a dictionnay. The key are the edges with a format 'p1,p2'. And the value is a counter of the number of face
    where (p1,p2) is in.

    Args:
        faces (np.array): An array with all the faces 

    Returns:
        dict: A dict
    """
    
    # Creation of the dict
    edges_dic = {}
    
    # Enumeration on all the faces
    for face in faces:
        
        # Creation of a list with the points of the face
        points = [face.a,face.b,face.c,face.a]
        
        # Enumeration on all the edges of the current face
        for i in range(3):
            
            # Creation of the associated key
            key = edg2key(points[i],points[i+1])
            
            # We check first if the edge is already represented in the dic
            if key in edges_dic:
                
                # If already in the dict, we increment the counter
                edges_dic[key] += 1
            
            else :
                
                # In the other case, we create a new key and set the counter to 1
                edges_dic[key] += 1

    # Return the list of edges
    return edges_dic




# def check_neighbour(edge, edges):
#     v1 = edge[0]
#     v2 = edge[1]
#     v1_neighbours = []
#     v2_neighbours = []
#     for e in edges:
#         ve_1 = e[0]
#         ve_2 = e[1]
#         if v1==ve_1:
#             v1_neighbours.append(ve_2)
#         elif v1==ve_2:
#             v1_neighbours.append(ve_1)
#         elif v2==ve_1:
#             v2_neighbours.append(ve_2)
#         elif v2==ve_2:
#             v2_neighbours.append(ve_1)
            
#     intersect = [v for v in v1_neighbours if v in v2_neighbours]
    
#     return len(intersect) <= 2