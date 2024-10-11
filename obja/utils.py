def edg2key(p1:int,p2:int):
    return str(p1) + "," + str(p2)


def create_dict_edges(faces):
    """Create a list with all the edges reguarding a list of all the faces

    Args:
        faces (np.array): The list of all the faces of the model
    """
    
    # Creation of the dict
    edges_dic = {}
    
    # Enumeration on all the faces
    for face in faces:
        
        if {face.a,face.b} in edges_dic.keys():
            edges_dic[{face.a,face.b}] += 1
        else:
            edges_dic[{face.a,face.b}] = 1
            
        if {face.b,face.c} in edges_dic.keys():
            edges_dic[{face.b,face.c}] += 1
        else:
            edges_dic[{face.b,face.c}] = 1
            
            
        if {face.a,face.c} in edges_dic.keys():
            edges_dic[{face.a,face.c}] += 1
        else:
            edges_dic[{face.a,face.c}] = 1

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