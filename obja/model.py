from obja import *
from transcriptionTable import *
import numpy as np


class ModelIteration(object):
    
    def __init__(self,iteration:int,faces:list,vertices:list):
        
        self.iteration = iteration
        self.__faces = faces
        self.__vertices = vertices
        
        if iteration == 0:
            self.__facesTable = TranscriptionTable("Iter " + str(iteration) + " facesTable",len(faces),"Identity")
            self.__verticesTable = TranscriptionTable("Iter " + str(iteration) + " verticesTable",len(faces),"Identity")
        else:
            self.__facesTable = TranscriptionTable("Iter " + str(iteration) + " facesTable",len(faces))
            self.__verticesTable = TranscriptionTable("Iter " + str(iteration) + " verticesTable",len(faces))
            
        
    def getFaces(self):
        return self.__faces
    
    def getVertices(self):
        return self.__vertices
     
    def getTranscriptionTable(self,objectType:str):
        if objectType == 'face':
            return self.__facesTable
        elif objectType == 'vertice':
            return self.__verticesTable
        else:
            raise KeyError
        
    def setTranscriptionTable(self,objectType:str,table:np.array):
        if objectType == 'face':
            self.__facesTable = table
        elif objectType == 'vertice':
            self.__verticesTable = table
        else:
            raise KeyError
        
class Model3D(object):
    
    def __init__(self,filename:str):
        
        # Create the main list
        self.__modelList = []
        
        # Get the initial model from the .obj file
        initModel = Model()
        initModel.parse_file('example/'+filename)
        
        # Create the ModelIteration object associated of the inital model
        self.__modelList.append(ModelIteration(0,initModel.faces,initModel.vertices))
        
        # Get the number of faces and vertices
        self.numberOfFaces = len(initModel.faces)
        self.numberOfVertices = len(initModel.vertices)
        
        
    def getLastModel(self):
        return self.__model[-1]
    
    def addModelIteration(self,iteration:int,faces:list,vertices:list,facesEvolution:list,verticesEvolution:list):
        
        # First of all, create a new ModelIteration
        model = ModelIteration(iteration,faces,vertices)
        
        # Now, we need to create the transcription table to save a link between the index of the initial model
        faceTable,verticeTable = self.createTranscriptionTable(model,facesEvolution,verticesEvolution)
        
        # Now set theses tables into the current model
        model.setTranscriptionTable('face',faceTable)
        model.setTranscriptionTable('vertice',verticeTable)
        
        # Finally, add this model into the modelList
        self.__modelList.append(model)

    
    def createTranscriptionTable(self,model:ModelIteration,facesEvolution:list,verticesEvolution:list):
        
        # iteration must be > 0
        if model.iteration > 0:
            raise NameError
        
        # We need to have the transcription table of the iteration 0, but it's only an identity, so let's recreate it
        faceTable = np.array([i for i in range(self.numberOfFaces)])
        verticeTable = np.array([i for i in range(self.numberOfVertices)])
        
        # The algorithm is simple : 
        #   When evolution[i] = 1 -> We do nothing
        #   When evolution[i] = 0 -> We remove the value with the index i of the list
        faceTable = [valeur for i, valeur in enumerate(faceTable) if facesEvolution[i] == 1]
        verticeTable = [valeur for i, valeur in enumerate(verticeTable) if verticesEvolution[i] == 1]
        
        return faceTable,verticeTable
        
        
"""
Objectif : En gros l'objectif c'est d'avoir un object (Model3D), qui regroupe l'évolution de notre modèle à chaque itération. On a donc
une variable model qui est une liste avec les modèles suivant les différentes itérations. Ca va nous permettre de bien séparer entre 
chaque itération, et voir si chaque modèle distinct est cohérent (en les affichant dans le future)

Le seul point clé, et de garder un lien entre l'indicage des élements (faces ou points) entre l'itération i et l'itération 0, histoire 
de ne pas d'avoir d'erreut, mais normalement, en regardant l'évolution et en se basant avec la table de transcription de l'itération
précédente ça doit passer.
"""
    