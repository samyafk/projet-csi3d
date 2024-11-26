from obja import *
from transcriptionTable import *
import numpy as np
import pyvista as pv
import math


class ModelIteration(object):
    
    def __init__(self,iteration:int,faces:list,vertices:list):
        
        self.iteration = iteration
        self.__faces = faces
        self.__vertices = vertices
            
        
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
        
    def display_model(self):
        """
        Visualizes the 3D object represented by the faces and vertices of the model.
        """
        mesh = self.get_3D_mesh()

        # Display the mesh
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color="lightblue", show_edges=True)
        plotter.show()
        
    def get_3D_mesh(self)->pv.PolyData:
        
        # Extract faces and vertices
        faces_list = self.getFaces()
        vertices_list = self.getVertices()

        # Convert vertices to a NumPy array
        vertices_array = np.array(vertices_list, dtype=np.float32)

        # PyVista expects a flattened array with the number of points at the beginning of each face
        faces_flat = []
        for face in faces_list:
            faces_flat.append([3, *[face[ind] for ind in range(len(face))]])
        faces_array = np.array(faces_flat)

        # Create a PyVista mesh
        mesh = pv.PolyData(vertices_array, faces_array)
        
        return mesh

        
class Model3D(object):
    
    def __init__(self,filename:str):
        
        # Create the main list
        self.__modelList = []
        
        # Get the initial model from the .obj file
        initModel = Model()
        initModel.parse_file('example/'+filename)
        
        # First convert the list of faces into a list of list
        faces = [[f.a,f.b,f.c] for f in initModel.faces]
        
        # Create the ModelIteration object associated of the inital model
        self.__modelList.append(ModelIteration(0,faces,initModel.vertices))
        
        # Get the number of faces and vertices
        self.numberOfFaces = len(initModel.faces)
        self.numberOfVertices = len(initModel.vertices)
        
        
    def getLastModel(self)->ModelIteration:
        return self.__modelList[-1]
    
    def addModelIteration(self,iteration:int,faces:list,vertices:list):
        
        # First of all, create a new ModelIteration
        model = ModelIteration(iteration,faces,vertices)
        
        # Finally, add this model into the modelList
        self.__modelList.append(model)
        

    def display_all_models(self):
        """
        Displays all ModelIteration objects stored in the Model3D instance.
        """
        # Get the number of different models
        numberModel = len(self.__modelList)
        
        # Dynamically calculate rows and columns for the grid
        nbrCol = 3  # Fixed number of columns
        nbrRows = math.ceil(numberModel / nbrCol)  # Dynamically compute rows
        
        # Create the plotter with the appropriate shape
        plotter = pv.Plotter(shape=(nbrRows, nbrCol))
        
        # Iterate through the models
        for iteration in range(numberModel):
            # Get the model and mesh
            model = self.__modelList[iteration]
            mesh = model.get_3D_mesh()
            
            # Calculate subplot position
            row = iteration // nbrCol
            col = iteration % nbrCol
            
            # Add the mesh to the plotter
            plotter.subplot(row, col)
            plotter.add_mesh(mesh, color="lightblue", show_edges=True)
            plotter.add_text(f"Iteration {iteration}")
        
        # Adjust camera and view
        plotter.view_isometric()
        
        # Show the plotter
        plotter.show()

        # Clean up resources
        plotter.close()
        
    import pyvista as pv

    def display_specific_iteration(self, iteration_index):
        """
        Displays a specific ModelIteration object by its index.

        Parameters:
        -----------
        iteration_index : int
            The index of the ModelIteration object to display.
        """
        # Ensure the index is valid
        if iteration_index < 0 or iteration_index >= len(self.__modelList):
            raise ValueError(f"Invalid iteration index {iteration_index}. Must be between 0 and {len(self.__modelList) - 1}.")
        
        # Get the model and its mesh
        model = self.__modelList[iteration_index]
        mesh = model.get_3D_mesh()
        
        # Create a new Plotter for this iteration
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color="lightblue", show_edges=True)
        plotter.add_text(f"Iteration {iteration_index}", font_size=10)
        plotter.view_isometric()
        
        # Show the plotter
        plotter.show()
        
        # Explicitly close the plotter to free resources
        plotter.close()




        

def main():
        
    # Create a 3DModel
    filename = 'suzanne.obj'
    model = Model3D(filename)
    
    # Get the last model (here its the 0)
    firstModel = model.getLastModel()
    
    # Display in 3D the model
    firstModel.display_model()
    
if __name__ == '__main__':
    main()