#!/usr/bin/env python

import obja
import numpy as np
from utils import *
from transcriptionTable import *
from obja import *
from writer import *
from tqdm import tqdm
from log import Logger

# TODO: ajouter le cas de la pondération à plus de 2 points

class Decimater(obja.Model):
    """A simple class that decimates a 3D model not so stupidly."""
    
    def __init__(self,filename:str,nbrIteration:int):
        super().__init__()
        
        self.parse_file('example/'+filename)
        
        self.nbrIteration = nbrIteration
        
        # List of list that have the evolution of the remaining faces through the iterations
        # 0 will indiq that the face is not here in this iteration
        # 1 will indiq that the face is again here
        self.faceEvolution = []
        
        # At the creation, all the face are here
        self.faceEvolution.append(np.ones(len(self.faces)))
        
        
        self.logger = Logger()
        
        self.writer = Writer(filename,len(self.vertices),len(self.faces),self.logger)

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
        """Going through one iteration of the squeeze method
        
        Args:
            currentIteration (int): the current iteration number
        """
        faces = self.retrieveFaces(currentIteration)
        
        # Create the list for the next iteration
        self.faceEvolution.append(self.faceEvolution[currentIteration])
        
        edges = self.conditions(faces)
        
        collapsed_vertices = []
        
        for key in edges:
            collapsible = edges[key]
            
            if not collapsible:
                pass
                
            edge = key2edg(key)
            
            v1 = edge[0]
            v2 = edge[1]
            
            if v1 in collapsed_vertices or v2 in collapsed_vertices:
                edges[key] = False
                pass
                
            collapsed_vertices.append(v1)
            collapsed_vertices.append(v2)
            
            coordVert1 = self.vertices[v1]
            coordVert2 = self.vertices[v2]
                        
            translation = (coordVert1 - coordVert2)/2

            # Collapse the edge
            for (face_index,present) in enumerate(self.faceEvolution[currentIteration]):
                if present:
                    face = self.faces[face_index]
                    
                    # Delete any face related to this edge
                    if v1 in [face.a,face.b,face.c] and v2 in [face.a,face.b,face.c]:
                        # Add 0 to the index of face_index (the face is deleted for the next iteration)
                        self.faceEvolution[currentIteration+1][face_index] = 0
                        
                        self.writer.operation_add_face(face_index,face)
                        
                    elif v2 in [face.a,face.b,face.c]:
                        # Translate the face
                        self.writer.operation_edit_face(face_index,obja.Face(face.a, face.b, face.c))
                        
                        # Check which vertex is the v2 and translate it
                        if v2 == face.a:
                            face.a = v1
                        elif v2 == face.b:
                            face.b = v1
                        elif v2 == face.c:
                            face.c = v1
            
            # Translate vertex1
            self.vertices[v1] = self.vertices[v1] + translation
            self.writer.operation_edit_vertex(v1,self.vertices[v1] -translation)
            
            # Delete vertex2 (no need to delete it from self.vertices 
            # bc we create edges using faces and it wont appear in the faces anymore)
            self.writer.operation_add_vertex(v2,self.vertices[v2])
            self.deleted_vertices.add(v2)        
    
    def conditions(self,faces:list) -> dict:
        """Create the dictionnary of the edges and checks the conditions
        
        Args:
            faces (list): list of the faces
            
        Returns:
            dict: dictionnary of the edges
        """
        edges = create_dict_edges(faces)
        edges = check_second_condition(edges)
        check_third_condition(edges)
        
        return edges
            
    def error(self):
        return None   
    
    def compression_algorithm(self) -> None:
        """Main function that will run CPM SQUEEZE algorithm
    
        """
        for i in range(self.nbrIteration):
            print("Number of faces :" + str(sum(self.faceEvolution[i])) + "\n")
            self.logger.msg_log("Number of faces :" + str(sum(self.faceEvolution[i])))
            self.reduce_face(i)
            
        # Add remaining vertices
        for (idx,v) in enumerate(self.vertices):
            if idx not in self.deleted_vertices:
                self.writer.operation_add_vertex(idx, v)
                                
        # add remaining faces
        for idx, (isPresent,face) in enumerate(zip(self.faceEvolution[-1],self.faces)):
            if isPresent:
                self.writer.operation_add_face(idx, face)
        
        try:
            self.writer.write_output()
            self.logger.save_log()
        except Exception as e:  # Catch and handle exceptions properly
            self.logger.msg_log(self.writer.faceTable)
            self.logger.msg_log(self.writer.pointTable)
            self.logger.err_log(e)
            
            raise e

def main():
    nbrIteration = 1
    
    filename = 'cube.obj'
    np.seterr(invalid = 'raise')
    
    model = Decimater(filename,nbrIteration)
    
    model.compression_algorithm()


if __name__ == '__main__':
    main()
