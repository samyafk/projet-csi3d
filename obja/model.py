from obja import *
from transcriptionTable import *

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

class Model3D(object):
    
    def __init__(self,filename:str):
        
        # Create the main list
        self.__model = []
        
        # Get the initial model from the .obj file
        initModel = Model()
        initModel.parse_file('example/'+filename)
        
        # Create the ModelIteration object associated of the inital model
        self.__model.append(ModelIteration(0,initModel.faces,initModel.vertices))
        
        # Get the number of faces and vertices
        self.numberOfFaces = len(initModel.faces)
        self.numberOfVertices = len(initModel.vertices)
        
        
    def getLastModel(self):
        return self.__model[-1]
    
    def addModelIteration(self,iteration:int,faces:list,vertices:list,facesEvolution:list,verticesEvolution:list):
        
        # First of all, create a new ModelIteration
        model = ModelIteration(iteration,faces,vertices)
        
        # Now, we need to create the transcription table to save a link between the index of the initial model
        faceTable = TranscriptionTable('Faces',len(faces))
        verticesTable = TranscriptionTable('vertices',len(vertices))
        
        # Now lets fill them
        currentIteration = iteration
        
        while currentIteration != 0:
            
            counter = 0
            
            for i in range(len(facesEvolution)):
                
                # Get the current evolution (ie : the face is still present or not in this new model)
                value = facesEvolution[i]
                
                if value == 1:
                    faceTable.addLink()
                    
        
        return None
    
    def createTranscriptionTable(self,iteration:int,numberOfElement:int,evolution:list,objectType:str='face'):
        
        # iteration must be > 0
        if iteration > 0:
            raise NameError
        
        # First create the transcription table and get the one from the last iteration
        if objectType == 'face':
            currentTable = TranscriptionTable("Iter " + str(iteration) + " facesTable",numberOfElement,"Identity")
            previousTable = self.__model[iteration-1].getTranscriptionTable('face')
        elif objectType == 'vertices':
            currentTable = TranscriptionTable("Iter " + str(iteration) + " verticesTable",numberOfElement,"Identity")
            previousTable = self.__model[iteration-1].getTranscriptionTable('vertice')
            
        counter = 0 
            
        # Now fill in the transcription table
        for i in range(evolution):
            
        
        
"""
Objectif : En gros l'objectif c'est d'avoir un object (Model3D), qui regroupe l'évolution de notre modèle à chaque itération. On a donc
une variable model qui est une liste avec les modèles suivant les différentes itérations. Ca va nous permettre de bien séparer entre 
chaque itération, et voir si chaque modèle distinct est cohérent (en les affichant dans le future)

Le seul point clé, et de garder un lien entre l'indicage des élements (faces ou points) entre l'itération i et l'itération 0, histoire 
de ne pas d'avoir d'erreut, mais normalement, en regardant l'évolution et en se basant avec la table de transcription de l'itération
précédente ça doit passer.
"""
    