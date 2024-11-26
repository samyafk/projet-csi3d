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


def create_list_edges(faces: Face) -> list:
    """Create a dictionnay. The key are the edges with a format 'p1,p2'. And the value is a counter of the number of face
    where (p1,p2) is in.

    Args:
        faces (Face): An array with all the faces 

    Returns:
        dict: A dict
    """
    edges_list = []
    
    for face in faces:
        points = [face.a,face.b,face.c,face.a]
        
        for i in range(3):
            key = edg2key(points[i],points[i+1])
            edges_list.append(key)

    return edges_list


def check_neighbour(edge: list, edges: list) -> bool:
    """Checks that the two vertices of the edge only have two neighbours in common
    
    Args:
        edge (list): the edge
        edges (dict): the dictionnary with the edges
        
    Returns:
        bool: True if the edge is collapsable, False otherwise
    """    
    v1, v2 = edge[0], edge[1]    
    v1_neighbours = neighbours(v1, edges)
    v2_neighbours = neighbours(v2, edges)
            
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


# Calculate the plane equation coefficients from three points
def calculate_plane(p1, p2, p3):
    # Calculate two directional vectors
    ab = p2 - p1
    ac = p3 - p1
    
    # Calculate the normal vector by cross product
    normal = np.cross(ab, ac)
    
    # Calculate d using the point p1
    d = -np.dot(normal, p1)
    
    # Return the plane coefficients (a, b, c, d)
    a, b, c = normal
    return (a, b, c, d)


# Calculate the error metrics on every edge of the object
def calculate_error_metrics(edges: list, faces: dict, vertices: dict):
    
    # Initialise the error metrics
    error_metrics = dict()

    # For each edge, calculate the error metric
    for key in edges:
        
        # Get the coordinates of the actual vertices and the future vertex
        edge = key2edg(key)
        v1 = np.array(vertices[edge[0]])
        v2 = np.array(vertices[edge[1]])
        new_vertex = v1 + v2 / 2      

        # Get the faces comprising them
        v1_faces = [face for idx, face in faces.items() if face.a == edge[0] or face.b == edge[0] or face.c == edge[0]]
        v2_faces = [face for idx, face in faces.items() if face.a == edge[1] or face.b == edge[1] or face.c == edge[1]]

        # Compute the Q matrix for v1 and v2 :
        # Get the fundamental error quadrics of the planes comprising those faces and add them to Q
        Q1 = np.zeros((4, 4))
        Q2 = np.zeros((4, 4))

        for face in v1_faces:
            p1, p2, p3 = vertices[face.a], vertices[face.b], vertices[face.c]
            a, b, c, d = calculate_plane(np.array(p1), np.array(p2), np.array(p3))
            K = np.array([[a**2, a*b, a*c, a*d],
                 [a*b, b**2, b*c, b*d],
                 [a*c, b*c, c**2, c*d],
                 [a*d, b*d, c*d, d**2]])
            Q1 += K
            

        for face in v2_faces:
            p1, p2, p3 = vertices[face.a], vertices[face.b], vertices[face.c]
            a, b, c, d = calculate_plane(np.array(p1), np.array(p2), np.array(p3))
            K = np.array([[a**2, a*b, a*c, a*d],
                 [a*b, b**2, b*c, b*d],
                 [a*c, b*c, c**2, c*d],
                 [a*d, b*d, c*d, d**2]])
            Q2 += K
            
        # Add the error metric to the dict : Q = Q1 + Q2
        Q = Q1 + Q2
        new_vertex_homogeneous = np.append(new_vertex, 1)
        error_metric = new_vertex_homogeneous @ Q @ new_vertex_homogeneous  # error_metric = new_vertex.T * Q * new_vertex
        error_metrics[key] = error_metric
        
    return error_metrics