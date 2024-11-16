from obja import *
from log import *
from writer import *
from model3D import *
from utils import *

class Compresser(object):

    def __init__(self, filename:str,numberOfIteration:int):
        
        # Create a 3DModel
        filename = 'suzanne.obj'
        self.__model = Model3D(filename)
        
        # Creation of the logger
        self.__logger = Logger()
        
        # Creation of the writter
        self.writer = Writer('example/'+filename, self.__model.numberOfVertices, self.__model.numberOfFaces, self.__logger)
        
        # The number of iteration
        self.numberOfIteration = numberOfIteration
        
    def contract(self,iteration:int):
        # Fonction qui fait une itération
        
        # Récupération du dernier model
        lastModel = self.__model.getLastModel()
        
        # On récupère les faces et les vertex encore présent
        faces = lastModel.getFaces()
        vertices = lastModel.getVertices()
        
        # On se base alors sur ces variables pour faire notre contraction
        
        # Create the dict with the edges
        edges = create_dict_edges(faces)
        
        # Calculate the error metrics
        error_metrics = calculate_error_metrics(edges, faces, vertices)
        
        # Reorder edges based on their error metrics
        sorted_edges = dict(sorted(error_metrics.items(), key=lambda item: item[1]))
        
        # Check second condition
        edges = check_second_condition(edges)
        
        # Check third condtition
        check_third_condition(edges)
        
        # Create list of collapsed vertices
        collapsed_vertices = []
        
        # For each edges in the dict
        for key in sorted_edges:
            
            collapsible = edges[key]
            # If second and third condition ok
            if collapsible:
                
                # Get the vertices of the edge
                edge = key2edg(key)
                
                # Check if one of the two already collapsed
                if edge[0] in collapsed_vertices or edge[1] in collapsed_vertices:
                    edges[key] = False
                    pass
                else:
                    
                    # Add the two vertex into the list : collapsed_vertices
                    collapsed_vertices.append(edge[0])
                    collapsed_vertices.append(edge[1])
                    
                    
                    # Get the coord of the first vertex
                    coordVert1 = self.vertices[edge[0]]
                    
                    # Get the coord of the second vertex
                    coordVert2 = self.vertices[edge[1]]
                    
                    # Compute the translation vector
                    t = (coordVert2 - coordVert1)/2
                    
                    # Collapse the edge
                    for (face_index, face) in enumerate(self.faces):
                        # Delete any face related to this edge
                        if face_index not in self.deleted_faces:
                            if edge[0] in [face.a,face.b,face.c] and edge[1] in [face.a,face.b,face.c]:
                                self.deleted_faces.add(face_index)
                                # Add the instruction to operations stack
                                self.writer.operation_add_face(face_index, face)
                            elif edge[1] in [face.a,face.b,face.c]:
                                self.writer.operation_edit_face(face_index, Face(face.a, face.b, face.c))
                                if edge[1] == face.a:
                                    face.a = edge[0]
                                elif edge[1] == face.b:
                                    face.b = edge[0]
                                elif edge[1] == face.c:
                                    face.c = edge[0]
                    
                    # Translate vertex1
                    self.vertices[edge[0]] = coordVert1 + t
                    self.writer.operation_edit_vertex(edge[0], self.vertices[edge[0]] - t)
                    
                    # Delete vertex2 (no need to delete it from self.vertices bc we create edges using faces and it wont appear in the faces anymore)
                    self.writer.operation_add_vertex(edge[1], coordVert2)
                    self.deleted_vertices.add(edge[1])
                    
                    # Update error metrics of edges involving vertex1 and vertex2
                    update_error_metrics(error_metrics, edge, edges, self.faces, self.vertices)
                    
        self.writer.operation_change_color_faces([0,0,0.3])
        
        # Arriver à récupérer une liste avec des 0 et des 1 pour les faces qui restent par rapport au modèle initiale
        
        # créer le nouveau modèle dans le modèle 3D
        
        return None
    
    def CPM(self):
        
        # Pour le nombre d'itération faire contract
        return None
        
        
        
        
    