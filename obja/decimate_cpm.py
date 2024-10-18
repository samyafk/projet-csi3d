#!/usr/bin/env python

import obja
import numpy as np
import sys
from utils import *

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()

    def contract(self, output):
        
        # Create the operations list
        operations = []
        
        # Create the dict with the edges
        edges = create_dict_edges(self.faces)
        
        # Check second condition
        edges = check_second_condition(edges)
        
        # Check third condtition
        check_third_condition(edges)
        
        # Create list of collapsed vertices
        collapsed_vertices = []
        
        # For each edges in the dict
        for key in edges:
            
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
                    
                    # Compute the mean of the vertex
                    mean = (coordVert1 + coordVert2)/2
                    
                    # Collapse the edge
                    for (face_index, face) in enumerate(self.faces):
                        # Delete any face related to this edge
                        if face_index not in self.deleted_faces:
                            if edge[0] in [face.a,face.b,face.c] and edge[1] in [face.a,face.b,face.c]:
                                self.deleted_faces.add(face_index)
                                # Add the instruction to operations stack
                                operations.append(('face', face_index, face))
                            elif edge[1] in [face.a,face.b,face.c]:
                                if edge[1] == face.a:
                                    operations.append(('ef', face_index, face))
                                    face.a = edge[0]
                                elif edge[1] == face.b:
                                    operations.append(('ef', face_index, face))
                                    face.b = edge[0]
                                elif edge[1] == face.c:
                                    operations.append(('ef', face_index, face))
                                    face.c = edge[0]
                    
                    # Translate vertex1
                    self.vertices[edge[0]] = mean
                    operations.append(('tv', edge[0], coordVert1 - mean))
                    
                    # Delete vertex2 (no need to delete it from self.vertices bc we create edges using faces and it wont appear in the faces anymore)
                    operations.append(('v', edge[1], coordVert2))
                    
                    
                        

            
            
        
        # operations = []
        # edges = create_dict_edges(self.faces)

        # collapse = [True for ]
        
        # print(edges)
        # print(collapse)
        
        # # Iterate through the vertex
        # for (vertex_index, vertex) in enumerate(self.vertices):

        #     # Iterate through the faces
        #     for (face_index, face) in enumerate(self.faces):

        #         # Delete any face related to this vertex
        #         if face_index not in self.deleted_faces:
        #             if vertex_index in [face.a,face.b,face.c]:
        #                 self.deleted_faces.add(face_index)
        #                 # Add the instruction to operations stack
        #                 operations.append(('face', face_index, face))

        #     # Delete the vertex
        #     operations.append(('vertex', vertex_index, vertex))

        # # To rebuild the model, run operations in reverse order
        # operations.reverse()

        # # Write the result in output file
        # output_model = obja.Output(output, random_color=True)

        # for (ty, index, value) in operations:
        #     if ty == "vertex":
        #         output_model.add_vertex(index, value)
        #     elif ty == "face":
        #         output_model.add_face(index, value)   
        #     else:
        #         output_model.edit_vertex(index, value)

def main():
    """
    Runs the program on the model given as parameter.
    """
    filename = 'suzanne.obj'
    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file('example/'+filename)
    with open('example/'+filename+'a', 'w') as output:
        model.contract(output)


if __name__ == '__main__':
    main()
