from warnings import warn
import numpy as np
from obja import Face

def edg2key(p1:int, p2:int) -> str:
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
    
    p1, p2 = map(int, key.split(","))
    
    return [p1, p2]
    


def create_dict_edges(faces: Face) -> dict:
    """Create a dictionnay. The key are the edges with a format 'p1,p2'. And the value is a counter of the number of face
    where (p1,p2) is in.

    Args:
        faces (Face): An array with all the faces 

    Returns:
        dict: A dict
    """
    
    edges_dic = {}
    
    for face in faces:
        points = [face.a,face.b,face.c,face.a]
        
        for i in range(3):
            edge = [points[i],points[i+1]]
            key = edg2key(points[i],points[i+1])
            edges_dic[key] = True

    return edges_dic

def check_second_condition(edges: dict) -> dict:
    """Check the second condition of the paper
    
    Args:
        edges (dict): a dictionnary with the edges
        
    Returns:
        dict: the dictionnary with the edges
    """
    
    for key in edges:
        edge = key2edg(key)
        edges[key] = check_neighbour(edge,edges)
        
    return edges


def check_neighbour(edge: list, edges: dict) -> bool:
    """Checks that the two vertices of the edge only have two neighbours in common
    
    Args:
        edge (list): the edge
        edges (dict): the dictionnary with the edges
        
    Returns:
        bool: True if the edge is collapsable, False otherwise
    """
    
    #FIXME fonction obselete (cf. neighbours)
    warn("fonction obselete (cf. neighbours) pour la mettre à jour", DeprecationWarning, stacklevel=2)
    
    v1, v2 = edge[0], edge[1]
    v1_neighbours, v2_neighbours = [], []
    
    for key in edges:
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
            
    intersect = [v for v in v1_neighbours if v in v2_neighbours]
    is_neighbour = len(intersect) <= 2
    
    return is_neighbour

def neighbours(vertex: int, edges: list) -> list:
    """Returns the neighbours of a given vertex
    
    Args:
        vertex (int): the vertex
        edges (list): the list of edges
        
    Returns:
        list: the list of neighbours
    """
    
    neighbours = []
    for e in edges:
        if vertex == e[0]:
            neighbours.append(e[1])
        elif vertex == e[1]:
            neighbours.append(e[0])
        
    return neighbours

# 
def vertex_tri(edge: list, edges: dict) -> tuple:
    """Checks that the two vertices of the edge only have 2 neighbours 
    in common and returns these neighbours
    
    Args:
        edge (list): the edge
        edges (dict): the dictionnary with the edges

    Returns:
        tuple: the two neighbours
    """
    
    v1, v2 = edge[0], edge[1]
    v1_neighbours = neighbours(v1, edges)
    v2_neighbours = neighbours(v2, edges)
            
    intersect = [v for v in v1_neighbours if v in v2_neighbours]
    
    if len(intersect) != 2:
        #TODO Gerer l'execption
        raise ValueError('Uh oh!')
    
    return intersect[0], intersect[1]

def check_quad(edge: list, edges: dict) -> None:
    """Checks if the neighbours are in the center of a quad
    If that's the case, set all the edges of the quad to non collapsable
    
    Args:
        edge (list): the edge
        edges (dict): the dictionnary with the edges
    """
    #FIXME optimiser les boucles de recherche de key/edge
    try:   
        w1, w2 = vertex_tri(edge, edges)
        
        w1_neighbours = neighbours(w1, edges)
        w2_neighbours = neighbours(w2, edges)
        
        if len(w1_neighbours) == 4:
            for i, j in range(4):
                key = edg2key(w1_neighbours[i], w1_neighbours[j])
                if key in edges.keys():
                    edges[key] = False
        
        if len(w2_neighbours) == 4:
            for i, j in range(4):
                key = edg2key(w2_neighbours[i], w2_neighbours[j])
                if key in edges.keys():
                    edges[key] = False
    except ValueError:
        pass

def check_third_condition(edges: dict) -> None:
    """Checks the third condition of the paper
    
    Args:
        edges (dict): the dictionnary with the edges
    """
    for key in edges:
        edge = key2edg(key)
        check_quad(edge, edges)

def computeTranslation(v1:np.array,v2:np.array,TYPE:str='mean') -> np.array:                    
    """
    Compute the translation vector between v1 and v2
    """      
    return (v1 - v2)/2