#!/usr/bin/env python

import obja
import numpy as np
import sys

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()

    def contract(self, output):
        
        operations = []
        edges = []

        for (face_index, face) in enumerate(self.faces):
            edges.append((face.a,face.b))
            edges.append((face.b,face.c))
            edges.append((face.a,face.c))

        collapse = [True for i in range(len(edges))]
        
        print(edges)
        #print(collapse)

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
    np.seterr(invalid = 'raise')
    model = Decimater()
    model.parse_file('example/suzanne.obj')

    with open('example/suzanne.obja', 'w') as output:
        model.contract(output)


if __name__ == '__main__':
    main()
