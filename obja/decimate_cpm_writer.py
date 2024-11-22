#!/usr/bin/env python

import obja
import numpy as np
from utils import *
from obja import Face
from writer import *
from log import *
from model3D import *
import time
import random
import matplotlib.pyplot as plt
import pyvista as pv


class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model stupidly.
    """
    def __init__(self,filename: str):
        super().__init__()
        self.parse_file('example/'+filename)
        self.deleted_faces = set()
        self.deleted_vertices = set()
        self.nb_of_faces_metrics = []
        self.nb_of_vertices_metrics = []
        self.iteration = 0
        self.logger = Logger()
        self.writer = Writer('example/'+filename, len(self.vertices), len(self.faces), self.logger)
        
        self.model3D = Model3D(filename)
    
    def plot_metrics(self):
        # This function plots the number of vertices and faces over the iterations
        iterations = np.arange(1, self.iteration)
        plt.plot(iterations, self.nb_of_faces_metrics, label='Number of Faces', color='blue')
        plt.plot(iterations, self.nb_of_vertices_metrics, label='Number of Vertices', color='red')
        plt.xlabel('Iterations')
        plt.ylabel('Number of Vertices and Faces')
        plt.legend()
        

        # Add legends
        plt.title('Number of Vertices and Faces over Iterations')
        plt.show()
        
        

    def CPM(self):
        
        # Create a dict of the vertices and the faces
        faces_dict = {i: face for i, face in enumerate(self.faces)}
        vertices_dict = {i: vertex for i, vertex in enumerate(self.vertices)}
        
        # The number of deleted vertices, to exit the while
        deleted_vertices_nb = 0
        
        # Number of iterations
        self.iteration = 1
        
        # Get current time
        start_time = time.time()
        total_time = 0

        stop = False
        while not stop:
            
            iteration_start_time = time.time()
            
            remainingFaces = [f for idx, f in faces_dict.items() if idx not in self.deleted_faces]
            self.nb_of_faces_metrics.append(len(remainingFaces))
            self.nb_of_vertices_metrics.append(len(vertices_dict) - len(self.deleted_vertices))
            
            # Create the dict with the edges
            edges = create_dict_edges(remainingFaces)
            
            # Calculate the error metrics
            error_metrics = calculate_error_metrics(edges, faces_dict, vertices_dict)
            
            # Reorder edges based on their error metrics
            sorted_edges = dict(sorted(error_metrics.items(), key=lambda item: item[1]))
            
            # Create list of collapsed vertices
            collapsed_vertices = []
            
            # For each edges in the dict
            for key in sorted_edges:
                   
                # Get the vertices of the edge
                edge = key2edg(key)
                
                # Check conditions
                collapsible = check_neighbour(edge, edges)

                # If conditions ok
                if not collapsible or edge[0] in collapsed_vertices or edge[1] in collapsed_vertices:
                    continue
                    
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
                            self.writer.operation_add_face(face_index,face)
                        elif edge[1] in [face.a,face.b,face.c]:
                            self.writer.operation_edit_face(face_index,Face(face.a, face.b, face.c))
                            if edge[1] == face.a:
                                face.a = edge[0]
                            elif edge[1] == face.b:
                                face.b = edge[0]
                            elif edge[1] == face.c:
                                face.c = edge[0]
                
                # Translate vertex1
                vertices_dict[edge[0]] = coordVert1 + t
                self.writer.operation_edit_vertex(edge[0],coordVert1)
                
                # Delete vertex2 (no need to delete it from self.vertices bc we create edges using faces and it wont appear in the faces anymore)
                self.writer.operation_add_vertex(edge[1],coordVert2)
                self.deleted_vertices.add(edge[1])                    
                # Update error metrics of edges involving vertex1 and vertex2
                update_error_metrics(error_metrics, edge, edges, faces_dict, vertices_dict)
                      
            # If no edge has been collapsed in the loop, get out from it
            if len(self.deleted_vertices) == deleted_vertices_nb:
                stop = True
                                
            # Get the numbers of vertices
            deleted_vertices_nb = len(self.deleted_vertices)
            
            # Get the remaining faces and vertices in order to create a model of the remaining info
            remainingFaces = [f for idx, f in faces_dict.items() if idx not in self.deleted_faces]
            remainingVertices = [v for idx, v in vertices_dict.items() if idx not in self.deleted_vertices]
            
            #FIXME
            # En gros y'a un probleme d'index des faces et donc les sous modèles sont mauvais            
            
            self.model3D.addModelIteration(self.iteration,remainingFaces,remainingVertices)
            
            # Change the color of the face
            self.writer.operation_change_color_faces([random.uniform(0.1, 0.5),random.uniform(0.1, 0.5),random.uniform(0.1, 0.5)],True)
            
            iteration_time = time.time() - iteration_start_time
            print("Iteration : " + str(self.iteration) + " - Total deleted vertices : " + str(deleted_vertices_nb) + " - Time : " + str(round(iteration_time,3)) + "s")
            self.iteration += 1
                
                
        # Add remaining faces
        for idx, f in faces_dict.items():
            if idx not in self.deleted_faces:
                self.writer.operation_add_face(idx,f)
        
        # Add remaining vertices
        for idx, v in vertices_dict.items():
            if idx not in self.deleted_vertices:
                self.writer.operation_add_vertex(idx,v)
                
        self.writer.write_output()
        
        total_time = time.time() - start_time
        print("\nTotal Time : " + str(round(total_time,3)) + "s")
        
    def display_model(self,iteration:int):
        
        self.model3D.display_specific_iteration(iteration)
        

def main():
    """
    Runs the program on the model given as parameter.
    """
    filename = 'suzanne.obj'
    np.seterr(invalid = 'raise')
    model = Decimater(filename)
    model.CPM()
    model.display_model(1)
    
    #model.plot_metrics()


if __name__ == '__main__':
    main()