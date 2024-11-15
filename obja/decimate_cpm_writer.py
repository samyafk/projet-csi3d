#!/usr/bin/env python

import obja
import numpy as np
import sys
from utils import *
from obja import Face
from log import *
from writer import *

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self, filename: str):
        super().__init__()
        
        self.parse_file('example/'+filename)
        
        self.deleted_faces = set()
        self.deleted_vertices = set()
        self.logger = Logger()
        self.writer = Writer('example/'+filename, len(self.vertices), len(self.faces), self.logger)

    def contract(self):
        
        # Create the dict with the edges
        edges = create_dict_edges(self.faces)
        
        # Calculate the error metrics
        error_metrics = calculate_error_metrics(edges, self.faces, self.vertices)
        
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
                    
        # Add remaining faces
        for (idx,f) in enumerate(self.faces):
            if idx not in self.deleted_faces:
                self.writer.operation_add_face(idx, f)
        
        # Add remaining vertices
        for (idx,v) in enumerate(self.vertices):
            if idx not in self.deleted_vertices:
                self.writer.operation_add_vertex(idx, v)

        # Write operations in the output file
        self.writer.write_output()

def main():
    """
    Runs the program on the model given as parameter.
    """
    filename = 'suzanne.obj'
    np.seterr(invalid = 'raise')
    model = Decimater(filename)
    model.contract()


if __name__ == '__main__':
    main()