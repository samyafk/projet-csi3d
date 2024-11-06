#!/usr/bin/env python

import obja
import numpy as np
import sys
from utils import *
from obja import Face

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()
        self.deleted_vertices = set()
        
    def iterate_faces(self, output):
        
        # Create the operations list
        operations = []
        
        # The difference between self.faces and self.deleted_faces
        remaining_faces = set([face for (idx, face) in enumerate(self.faces) if idx not in self.deleted_faces])
        
        # Create the dict with the edges
        edges = create_dict_edges(remaining_faces)
        
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
                    
                    # Compute the translation vector
                    t = (coordVert2 - coordVert1)/2
                    
                    # Collapse the edge
                    for (face_index, face) in enumerate(self.faces):
                        # Delete any face related to this edge
                        if face_index not in self.deleted_faces:
                            if edge[0] in [face.a,face.b,face.c] and edge[1] in [face.a,face.b,face.c]:
                                self.deleted_faces.add(face_index)
                                # Add the instruction to operations stack
                                operations.append(('f', face_index, face))
                            elif edge[1] in [face.a,face.b,face.c]:
                                operations.append(('ef', face_index, Face(face.a, face.b, face.c)))
                                if edge[1] == face.a:
                                    face.a = edge[0]
                                elif edge[1] == face.b:
                                    face.b = edge[0]
                                elif edge[1] == face.c:
                                    face.c = edge[0]
                    
                    # Translate vertex1
                    self.vertices[edge[0]] = coordVert1 + t
                    operations.append(('tv', edge[0], -t))
                    
                    # Delete vertex2 (no need to delete it from self.vertices bc we create edges using faces and it wont appear in the faces anymore)
                    operations.append(('v', edge[1], coordVert2))
                    self.deleted_vertices.add(edge[1])
                    

                    
        # To rebuild the model, run operations in reverse order
        operations.reverse()

        # Write the result in output file
        output_model = obja.Output(output, random_color=True)
        
        # Add remaining vertices
        for (idx,v) in enumerate(self.vertices):
            if idx not in self.deleted_vertices:
                output_model.add_vertex(idx, v)
                
        # add remaining faces
        for (idx,f) in enumerate(self.faces):
            if idx not in self.deleted_faces:
                output_model.add_face(idx, f)

        
        for (ty, index, value) in operations:
            
            if ty == "v":
                output_model.add_vertex(index, value)
            elif ty == "f":
                output_model.add_face(index, value)  
            elif ty == "tv":
                output_model.edit_vertex(index, self.vertices[index] + value)
            elif ty == "ef":
                output_model.edit_face(index, value)        
            else:
                output_model.edit_vertex(index, value)
                
    def iterate_faces_new(self,remaining_faces):
        
        # Create the current operations list
        currentOperations = []
        
        # Create the dict with the edges
        edges = create_dict_edges(remaining_faces)
        
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
                    
                    # Compute the translation vector
                    t = (coordVert2 - coordVert1)/2
                    
                    # Collapse the edge
                    for (face_index, face) in enumerate(self.faces):
                        
                        # Check if the face in the remaining_faces
                        if face in remaining_faces:
                            
                            # Delete any face related to this edge
                            if edge[0] in [face.a,face.b,face.c] and edge[1] in [face.a,face.b,face.c]:
                                
                                # Add the face to the deleted_faces
                                self.deleted_faces.add(face_index)
                                
                                # Add the instruction to operations stack
                                currentOperations.append(('f', face_index, face))
                                
                            # Check if the edge[1] is in the face
                            elif edge[1] in [face.a,face.b,face.c]:
                                
                                # Translate the face
                                currentOperations.append(('ef', face_index, Face(face.a, face.b, face.c)))
                                
                                # Check which vertex is the edge[1] and translate it
                                if edge[1] == face.a:
                                    self.faces[face_index].a = edge[0]
                                    face.a = edge[0]
                                elif edge[1] == face.b:
                                    face.b = edge[0]
                                elif edge[1] == face.c:
                                    face.c = edge[0]
                    
                    # Translate vertex1
                    self.vertices[edge[0]] = coordVert1 + t
                    currentOperations.append(('tv', edge[0], -t))
                    
                    # Delete vertex2 (no need to delete it from self.vertices bc we create edges using faces and it wont appear in the faces anymore)
                    currentOperations.append(('v', edge[1], coordVert2))
                    self.deleted_vertices.add(edge[1])
                    
        return currentOperations

    def contract(self, output):
        
        operations = []
        
        i=0
        while i < 5:

            # The difference between self.faces and self.deleted_faces
            remaining_faces = set([face for (idx, face) in enumerate(self.faces) if idx not in self.deleted_faces])
            
            currentOperations = Decimater.iterate_faces_new(self,remaining_faces)
            i+=1
            
            operations = operations + currentOperations
        
        # To rebuild the model, run operations in reverse order
        operations.reverse()

        # Write the result in output file
        output_model = obja.Output(output, random_color=True)
        
        # Add remaining vertices
        for (idx,v) in enumerate(self.vertices):
            if idx not in self.deleted_vertices:
                output_model.add_vertex(idx, v)
                
        # add remaining faces
        for (idx,f) in enumerate(self.faces):
            if idx not in self.deleted_faces:
                output_model.add_face(idx, f)

        
        for (ty, index, value) in operations:
            
            if ty == "v":
                output_model.add_vertex(index, value)
            elif ty == "f":
                output_model.add_face(index, value)  
            elif ty == "tv":
                output_model.edit_vertex(index, self.vertices[index] + value)
            elif ty == "ef":
                output_model.edit_face(index, value)        
            else:
                output_model.edit_vertex(index, value)
        

        

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
