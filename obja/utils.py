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
    
    
def key2edg(key: str) -> list:
    """Convert a str key back into two points 

    Args:
        key (str): the key in the format 'p1,p2'

    Returns:
        tuple: a tuple of two integers (p1, p2)
    """
    
    # Split the key 
    p1, p2 = map(int, key.split(","))
    
    return [p1, p2]
    


def create_dict_edges(faces):
    """Create a dictionnay. The key are the edges with a format 'p1,p2'. And the value is a counter of the number of face
    where (p1,p2) is in.

    Args:
        faces (?): An array with all the faces 

    Returns:
        dict: A dict
    """
    
    # Creation of the dict
    edges_dic = {}
    
    # Enumeration on all the faces
    for face in faces:
        
        # Creation of a list with the points of the face
        points = [face[0],face[1],face[2],face[0]]
        
        # Enumeration on all the edges of the current face
        for i in range(3):
            
            # Creation of edge
            edge = [points[i],points[i+1]]
            
            # Creation of the associated key
            key = edg2key(points[i],points[i+1])

            # Set collapsable to true
            edges_dic[key] = True

    # Return the list of edges
    return edges_dic

def check_second_condition(edges):
    
    for key in edges:
        
        # Get the points
        edge = key2edg(key)
        
        # Check with the neighboor
        edges[key] = check_neighbour(edge,edges)
        
    return edges


def check_neighbour(edge, edges):
    
    # get the first vertice
    v1 = edge[0]
    
    # get the second vertice
    v2 = edge[1]
    
    # Create empty lists
    v1_neighbours = []
    v2_neighbours = []
    
    # For each edges
    for key in edges:
        
        # Get vertices of the current edge (e)
        (ve_1,ve_2) = key2edg(key)
        
        # Check if ve_1 or ve_2 are in the neighbourhoods
        if v1==ve_1:
            v1_neighbours.append(ve_2)
        if v1==ve_2:
            v1_neighbours.append(ve_1)
        if v2==ve_1:
            v2_neighbours.append(ve_2)
        if v2==ve_2:
            v2_neighbours.append(ve_1)
            
    # Intersect
    intersect = [v for v in v1_neighbours if v in v2_neighbours]
    
    return len(intersect) <= 2