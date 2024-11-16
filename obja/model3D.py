from obja import *
from transcriptionTable import *
import numpy as np
import pyvista as pv


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
        
    def display_model(self):
        """
        Visualizes the 3D object represented by the faces and vertices of the model.
        """
        # Extract faces and vertices
        faces_list = self.getFaces()
        vertices_list = self.getVertices()

        # Convert vertices to a NumPy array
        vertices_array = np.array(vertices_list, dtype=np.float32)

        # PyVista expects the faces array to include the number of points in each face
        faces_with_sizes = []
        for face in faces_list:
            faces_with_sizes.append([3,face.a,face.b,face.c])
        faces_array = np.array(faces_with_sizes, dtype=np.int32)

        # Create a PyVista mesh
        mesh = pv.PolyData(vertices_array, faces_array)

        # Display the mesh
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color="lightblue", show_edges=True)
        plotter.show()
        
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
        
        
    def getLastModel(self)->ModelIteration:
        return self.__modelList[-1]
    
    def addModelIteration(self,iteration:int,faces:list,vertices:list,facesEvolution:list,verticesEvolution:list):
        
        # First of all, create a new ModelIteration
        model = ModelIteration(iteration,faces,vertices)
        
        # Now, we need to create the transcription table to save a link between the index of the initial model
        faceTable,verticeTable = self.__createTranscriptionTable(model,facesEvolution,verticesEvolution)
        
        # Now set theses tables into the current model
        model.setTranscriptionTable('face',faceTable)
        model.setTranscriptionTable('vertice',verticeTable)
        
        # Finally, add this model into the modelList
        self.__modelList.append(model)

    
    def __createTranscriptionTable(self,model:ModelIteration,facesEvolution:list,verticesEvolution:list):
        
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
        

def main():
        
    # Create a 3DModel
    filename = 'cube.obj'
    model = Model3D(filename)
    
    # Get the last model (here its the 0)
    firstModel = model.getLastModel()
    
    # Display in 3D the model
    firstModel.display_model()
    
if __name__ == '__main__':
    main()