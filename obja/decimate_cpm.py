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
        
        # Create the dict with the edges
        edges = create_dict_edges(self.faces)
        
        # Resolve the third condition -> Create a graph (nx lib) and check for cycle of length 4
        
        # For each edges in the dict
        
            # Check if the number is < 3
            
            # Check is the edges is not in a cycle of 4 (we can just have a long list with all the edges in a cycle of 4)
            
            # Check if one point of the two (in the edge) have a link with an edge already collapsed
            
            # If collapsable : 
            
                # collapse the edge
                
                # Add p1 and p2 in a list -> for the third check
            
            
        
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
    filename = 'schema_b.obj'
    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file('example/'+filename)

    with open('example/'+filename+'a', 'w') as output:
        model.contract(output)


if __name__ == '__main__':
    main()
