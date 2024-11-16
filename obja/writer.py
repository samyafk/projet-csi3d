from transcriptionTable import *
from log import *
import random
from tqdm import tqdm
from obja import *


class IndexPointExceedError(Exception):
    def __init__(self, message="Too much point reguarding the inital number of points value"):
        self.message = f"{message}"
        super().__init__(self.message)
        
class IndexFaceExceedError(Exception):
    def __init__(self, message="Too much point reguarding the inital number of face value"):
        self.message = f"{message}"
        super().__init__(self.message)

class Writer(object):
    
    def __init__(self,outputFile:str,nbrPoints:int,nbrFaces:int,logger:Logger=None):
        self.operations = []
        self.outputFile = outputFile
        self.faceTable = TranscriptionTable("Faces",nbrFaces)
        self.pointTable = TranscriptionTable("Points",nbrPoints)
        self.logger = logger
        
        self.faceCounter = 0
        self.pointCounter = 0
        
    def incrementPointCounter(self) -> None:
        exceed_gesture = self.pointCounter == self.pointTable.len()
        
        if exceed_gesture:
            raise IndexPointExceedError()
        else:
            self.pointCounter += 1
            
    def incrementFaceCounter(self) -> None:
        exceed_gesture = self.faceCounter == self.faceTable.len()
        
        if exceed_gesture:
            raise IndexFaceExceedError()
        else:
            self.faceCounter += 1
    
    def operation_add_vertex(self,indexModel:int,value:list) -> None:
        """Add a vertex into the operation stack
        
        Args:
            indexModel (int): the index of the model
            value (list): the value of the vertex
        """
        self.operations.append(('v',indexModel, value))
        
        if self.logger != None:
            self.logger.msg_log('Add vertex : ' + str(indexModel))
    
    def operation_add_face(self,indexModel:int,value:Face) -> None:
        """Add a face into the operation stack
        
        Args:
            indexModel (int): the index of the model
            value (Face): the value of the face
        """
        self.operations.append(('f',indexModel, value))
        
        if self.logger != None:
            self.logger.msg_log('Add face : ' + str(indexModel))
        
    def operation_edit_vertex(self,indexModel:int,newValue:list) -> None:
        """Edit a vertex into the operation stack
        
        Args:
            indexModel (int): the index of the model
            newValue (list): the new value of the vertex
        """    
        self.operations.append(('ev',indexModel,newValue))
        
        if self.logger != None:
            self.logger.msg_log('Edit vertex : ' + str(indexModel))
    
    def operation_edit_face(self, indexModel:int,newValue:Face) -> None:
        """Edit a face into the operation stack
        
        Args:
            indexModel (int): the index of the model
            newValue (Face): the new value of the face
        """         
        self.operations.append(('ef',indexModel,newValue))
        
        if self.logger != None:
            self.logger.msg_log('Edit face : ' + str(indexModel))
        
    def operation_change_color_faces(self,color:list) -> None:
        """Change the color of the faces"""
        self.operations.append(('color',0,color))
        
    def __faceIndexModel_2_faceObjaModel(self,face:Face) -> list:
        """Convert the index of the face from the model to the obja index
        
        Args:
            face (Face): the face
            
        Returns:
            list: the list of the index of the face in the obja file
        """
        a = self.pointTable.getObjaInd(face.a)
        b = self.pointTable.getObjaInd(face.b)
        c = self.pointTable.getObjaInd(face.c)
        
        return [a,b,c]
        
    def __add_vertex_output(self,indexModel:int, vertex:list) -> None:
        """Add a vertex into the output file
        
        Args:
            indexModel (int): the index of the model
            vertex (list): the value of the vertex
        """
        self.pointTable.addLink(indexModel,self.pointCounter)
        
        self.incrementPointCounter()
        
        # Add the vertex into the output file
        print('v {} {} {}'.format(vertex[0], vertex[1], vertex[2]), file=self.outputFile)
        
    def __add_face_output(self,indexModel:int,face:Face,color:list=None) -> None:
        """Add a face into the output file

        Args:
            indexModel (int): the index of the model
            face (Face): the face
            color (list): the color of the face
        """
        self.faceTable.addLink(indexModel,self.faceCounter)
        
        self.incrementFaceCounter()
        
        indexObja = self.faceTable.getObjaInd(indexModel)
        
        pointFaceObja = self.__faceIndexModel_2_faceObjaModel(face)

        # Add the face into the output file        
        print('f {} {} {}'.format(pointFaceObja[0] + 1, pointFaceObja[1] + 1, pointFaceObja[2] + 1), file=self.outputFile)
        
        # Add color to the face
        if color != None:
            print('fc {} {} {} {}'.format(indexObja+1,color[0],color[1],color[2]),file=self.outputFile)
                    
    def __edit_vertex_ouput(self,indexModel:int,vertex:list) -> None:
        """Edit a vertex into the output file
        
        Args:
            indexModel (int): the index of the model
            vertex (list): the new value of the vertex
        """
        indexObja = self.pointTable.getObjaInd(indexModel)
        
        print('ev {} {} {} {}'.format(indexObja+1,vertex[0], vertex[1], vertex[2]), file=self.outputFile)
        
    def __edit_face_output(self,indexModel:int,face:Face,color:list=None) -> None:
        """Edit a face into the output file
        
        Args:
            indexModel (int): the index of the model
            face (Face): the new face
            color (list): the color of the face
        """
        indexObja = self.faceTable.getObjaInd(indexModel)
        
        pointFaceObja = self.__faceIndexModel_2_faceObjaModel(face)
        
        print('ef {} {} {} {}'.format(indexObja+1,pointFaceObja[0] + 1, pointFaceObja[1] + 1, pointFaceObja[2] + 1), file=self.outputFile)
        
        if color != None:
            print('fc {} {} {} {}'.format(indexObja+1,color[0],color[1],color[2]),file=self.outputFile)
        
        
    def write_output(self) -> None:
        """Write the output file"""
        print("Start writing the output file \n")
        
        # Now defind a color for the faces
        gray_value = 0.5  
        color = [gray_value, gray_value, gray_value]
        
        reverseOperations = self.operations[::-1]
        
        with open(self.outputFile+'a', 'w') as self.outputFile:
        
            for (ty, indexModel, value) in tqdm(reverseOperations,desc="Écriture dans le fichier"):
                
                if ty == "v":
                    self.__add_vertex_output(indexModel,value)
                elif ty == "f":
                    self.__add_face_output(indexModel, value, color)  
                elif ty == "ev":
                    self.__edit_vertex_ouput(indexModel, value)
                elif ty == "ef":
                    self.__edit_face_output(indexModel, value)   
                elif ty == "color":
                    color = value     
                else:
                    raise SyntaxError("Too understand the type")
            
        # Finnally, check if the two table are bijective
        self.faceTable.isBijective()
        self.pointTable.isBijective()
            
        print("Ouput File sucesfully write !")
        
        
def main():
        
    print('test')
        
    model = parse_file('example/cube.obj')
        
    writer = Writer('example/prout.obj',len(model.vertices),len(model.faces))
         
    # Add the points and the faces into the operation list
    for (indexModel,face) in enumerate(model.faces):
        writer.operation_add_face(indexModel,face)
        
    for (indexModel,vertice) in enumerate(model.vertices):
        writer.operation_add_vertex(indexModel,vertice)
        
    try:
        writer.write_output()
    except Exception as e:  # Catch and handle exceptions properly
        print("An error occurred while writing the output:")
        print(e)
        print("Face table:", writer.faceTable)
        print("Point table:", writer.pointTable)
        # Optionally re-raise the exception
        raise 
    
if __name__ == '__main__':
    main()