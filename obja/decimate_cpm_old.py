#!/usr/bin/env python

import obja
import numpy as np
from utils import *
from obja import Face
import time

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self):
        super().__init__()
        self.deleted_faces = set()
        self.deleted_vertices = set()

    def contract(self, output):
        
        # Create the operations list
        operations = []
        
        # Create a dict of the vertices and the faces
        faces_dict = {i: face for i, face in enumerate(self.faces)}
        vertices_dict = {i: vertex for i, vertex in enumerate(self.vertices)}
        
                    
        # The number of deleted vertices, to exit the while
        deleted_vertices_nb = 0
        
        # Number of iterations
        iteration = 1
        
        # Get current time
        start_time = time.time()
        total_time = 0

        stop = False
        while not stop:
            
            iteration_start_time = time.time()
            
            # Create the dict with the edges
            edges = create_dict_edges([f for idx, f in faces_dict.items() if idx not in self.deleted_faces])
            
            # Calculate the error metrics
            error_metrics = calculate_error_metrics(edges, faces_dict, vertices_dict)
            
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
                if not collapsible:
                    continue
                    
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
                    coordVert1 = vertices_dict[edge[0]]
                    
                    # Get the coord of the second vertex
                    coordVert2 = vertices_dict[edge[1]]
                    
                    # Compute the translation vector
                    t = (coordVert2 - coordVert1)/2
                    
                    # Collapse the edge
                    for face_index, face in faces_dict.items():
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
                    vertices_dict[edge[0]] = coordVert1 + t
                    operations.append(('ev', edge[0], coordVert1))
                    
                    # Delete vertex2 (no need to delete it from self.vertices bc we create edges using faces and it wont appear in the faces anymore)
                    operations.append(('v', edge[1], coordVert2))
                    self.deleted_vertices.add(edge[1])
                    
                    # Update error metrics of edges involving vertex1 and vertex2
                    update_error_metrics(error_metrics, edge, edges, faces_dict, vertices_dict)
                        
            # If no edge has been collapsed in the loop, get out from it
            if len(self.deleted_vertices) == deleted_vertices_nb:
                stop = True
                
            deleted_vertices_nb = len(self.deleted_vertices)
            
            iteration_time = time.time() - iteration_start_time
            print("Iteration : " + str(iteration) + " - Total deleted vertices : " + str(deleted_vertices_nb) + " - Time : " + str(round(iteration_time,3)) + "s")
            iteration += 1
                
        # To rebuild the model, run operations in reverse order
        operations.reverse()

        # Write the result in output file
        output_model = obja.Output(output, random_color=True)
        
        # Add remaining vertices
        for idx, v in vertices_dict.items():
            if idx not in self.deleted_vertices:
                output_model.add_vertex(idx, v)
                
        # Add remaining faces
        for idx, f in faces_dict.items():
            if idx not in self.deleted_faces:
                output_model.add_face(idx, f)

        
        for (ty, index, value) in operations:
            
            if ty == "v":
                output_model.add_vertex(index, value)
            elif ty == "f":
                output_model.add_face(index, value)  
            elif ty == "ev":
                output_model.edit_vertex(index, value)
            elif ty == "ef":
                output_model.edit_face(index, value)        
            else:
                output_model.edit_vertex(index, value)
        
        total_time = time.time() - start_time
        print("\nTotal Time : " + str(round(total_time,3)) + "s")
        

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