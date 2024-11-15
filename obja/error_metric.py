import numpy as np
from utils import key2edg

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
def calculate_error_metrics(edges: dict, faces: list):
    
    # Initialise the error metrics
    error_metrics = dict()

    # For each edge, calculate the error metric
    for key in edges:
        
        # Get the coordinates of the actual vertices and the future vertex
        edge = key2edg(key)
        v1 = np.array(edge[0])
        v2 = np.array(edge[1])
        new_vertex = v1 + v2 / 2      

        # Get the faces comprising them
        v1_faces = [face for face in faces if face.a == v1 or face.b == v1 or face.c == v1]
        v2_faces = [face for face in faces if face.a == v2 or face.b == v2 or face.c == v2]

        # Compute the Q matrix for v1 and v2 :
        # Get the fundamental error quadrics of the planes comprising those faces and add them to Q
        Q1 = np.zeros((4, 4))
        Q2 = np.zeros((4, 4))

        for face in v1_faces:
            p1, p2, p3 = face.a, face.b, face.c
            a, b, c, d = calculate_plane(np.array(p1), np.array(p2), np.array(p3))
            K = np.array([[a**2, a*b, a*c, a*d],
                 [a*b, b**2, b*c, b*d],
                 [a*c, b*c, c**2, c*d],
                 [a*d, b*d, c*d, d**2]])
            Q1 += K
            

        for face in v2_faces:
            p1, p2, p3 = face.a, face.b, face.c
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