#!/usr/bin/env python

import obja
import numpy as np
import sys
from utils import *
from transcriptionTable import *
from obja import Face
from writer import *
from tqdm import tqdm

class Decimater(obja.Model):
    """
    A simple class that decimates a 3D model not so stupidly.
    """
    def __init__(self,filename:str,nbrIteration:int):
        
        # self.faces -> List
        # self.vertices -> List
        super().__init__()
        
        # Reading of the object
        self.parse_file('example/'+filename)
        
        # Number of iterations
        self.nbrIteration = nbrIteration
        
        
        # List of list that have the evolution of the remaining faces through the iterations
        # 0 will indiq that the face is not here in this iteration
        # 1 will indiq that the face is again here
        self.faceEvolution = []
        
        # At the creation, all the face are here
        self.faceEvolution.append(np.ones(len(self.faces)))
        
        # Create the writer
        self.writer = Writer(filename,len(self.vertices),len(self.faces))

        # List of the deleted vertices
        self.deleted_vertices = set()
        
    def retrieveFaces(self,currentIteration:int) -> list:
        """Retrieve the remaining faces for the current iteration

        Args:
            currentIteration (int): the iteration you want

        Returns:
            array: array of the remaining faces according to the iteration number
        """
        return [array for array, binary in zip(self.faces, self.faceEvolution[currentIteration]) if binary == 1]
        
         
    def reduce_face(self,currentIteration:int) -> None:
        """
        Goinng through one iteration of the squeeze method
        """
        
        # Retrieve the remaining faces for the current iteration
        faces = self.retrieveFaces(currentIteration)
        
        # Create the list for the next iteration
        self.faceEvolution.append(self.faceEvolution[currentIteration])
        
        # Create the edges dictionnary and check some conditions
        edges = self.conditions(faces)
        
        # Create list of collapsed vertices
        collapsed_vertices = []
        
        # For each edges in the dict
        for key in edges:
            
            # We look if we can collapse this edge
            collapsible = edges[key]
            if collapsible:
                
                # Get the vertices of the edge
                edge = key2edg(key)
                
                # Check if one of the two already collapsed
                if edge[0] in collapsed_vertices or edge[1] in collapsed_vertices:
                    edges[key] = False
                    pass
                else:
                    
                    #FIXME ajouter le cas de la pondération à plus de 2 points
                    # Get the index of the two vertices and add it into the collapsed_vertices list
                    v1 = edge[0]; collapsed_vertices.append(v1)
                    v2 = edge[1]; collapsed_vertices.append(v2)
                              
                    # Compute the translation
                    t = computeTranslation([v1,v2],'mean')

                    # Collapse the edge
                    for (face_index,present) in enumerate(self.faceEvolution[currentIteration]):
                        
                        # If the face is present in this iteration
                        if present:
                            
                            # Get the face
                            face = self.faces[face_index]
                            
                            # Delete any face related to this edge
                            if edge[0] in [face.a,face.b,face.c] and edge[1] in [face.a,face.b,face.c]:
                                
                                # Add 0 to the index of face_index (the face is deleted for the next iteration)
                                self.faceEvolution[currentIteration+1][face_index] = 0
                                
                                # Add the instruction to operations stack (Create a new face)
                                print("Add face : " + str(face_index) + "\n")
                                self.writer.operation_add_face(face_index,face)
                                
                            # Check if the edge[1] is in the face
                            elif edge[1] in [face.a,face.b,face.c]:
                                
                                # Translate the face
                                print("Edit face : " + str(face_index) + "\n")
                                self.writer.operation_edit_face(face_index,Face(face.a, face.b, face.c))
                                
                                # Check which vertex is the edge[1] and translate it
                                if edge[1] == face.a:
                                    self.faces[face_index].a = edge[0]
                                    face.a = edge[0]
                                elif edge[1] == face.b:
                                    self.faces[face_index].b = edge[0]
                                    face.b = edge[0]
                                elif edge[1] == face.c:
                                    self.faces[face_index].c = edge[0]
                                    face.c = edge[0]
                    
                    # Translate vertex1
                    self.vertices[edge[0]] = self.vertices[v1] + t
                    print("Edit vertex : " + str(edge[0]) + "\n")
                    self.writer.operation_edit_vertex(edge[0],self.vertices[v1] -t)
                    
                    # Delete vertex2 (no need to delete it from self.vertices bc we create edges using faces and it wont appear in the faces anymore)
                    self.writer.operation_add_vertex(edge[1],self.vertices[v2])
                    print("Add vertex : " + str(edge[1]) + "\n")
                    self.deleted_vertices.add(edge[1])        
    
    def conditions(self,faces:list) -> dict:
        """
        Create the dictionnary of the edges and checks the conditions
        """
        
        # Create the dict with the edges
        edges = create_dict_edges(faces)
        
        # Check second condition
        edges = check_second_condition(edges)
        
        # Check third condtition
        check_third_condition(edges)
        
        return edges
            
    def error(self):
        return None   
    
    def compression_algorithm(self) -> None:
        
        # Run the compression
        for i in range(self.nbrIteration):
            print("Number of faces :" + str(sum(self.faceEvolution[i])) + "\n")
            self.reduce_face(i)
            
        # Add the remaining point and faces
        # Add remaining vertices
        for (idx,v) in enumerate(self.vertices):
            if idx not in self.deleted_vertices:
                self.writer.operation_add_vertex(idx, v)
                                
        # add remaining faces
        for idx, (isPresent,face) in enumerate(zip(self.faceEvolution[-1],self.faces)):
            if isPresent:
                self.writer.operation_add_face(idx, face)
        
        # Write the obja file
        self.writer.write_output()

def main():
    """
    Runs the program on the model given as parameter.
    """
    
    # Number of iterations
    nbrIteration = 1
    
    filename = 'cube.obj'
    np.seterr(invalid = 'raise')
    
    model = Decimater(filename,nbrIteration)
    
    model.compression_algorithm()


if __name__ == '__main__':
    main()
