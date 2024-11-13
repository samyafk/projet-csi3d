from transcriptionTable import *
from obja import *
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

class Writter(object):
    
    def __init__(self,outputFile:str,nbrPoints:int,nbrFaces:int):
        self.operations = []
        self.outputFile = outputFile
        self.faceTable = TranscriptionTable("Faces",nbrFaces)
        self.pointTable = TranscriptionTable("Points",nbrPoints)
        
        self.faceCounter = 0
        self.pointCounter = 0
        
    def incrementPointCounter(self):
        # Exceed Gesture
        if self.pointCounter == self.pointTable.len():
            raise IndexPointExceedError()
        else:
            self.pointCounter += 1
            
    def incrementFaceCounter(self):
        # Exceed gesture
        if self.faceCounter == self.faceTable.len():
            raise IndexFaceExceedError()
        else:
            self.faceCounter += 1
        
    
    def operation_add_vertex(self,indexModel:int,value:list):
        
        # # First we need to create a link in the transcription table
        # self.pointTable.addLink(indexModel,self.pointCounter)
        
        # # We increment the pointCounter variable as this index is already taken
        # self.incrementPointCounter()
        
        # # Get the index value in the obja file
        # indexObja = self.pointTable.getObjaInd(indexModel)
        
        # Add the operation into the operation list
        self.operations.append(('v',indexModel, value))
    
    def operation_add_face(self,indexModel:int,value:Face):
        
        # # First we need to create a link in the transcription table
        # self.faceTable.addLink(indexModel,self.faceCounter)
        
        # # We increment the pointCounter variable as this index is already taken
        # self.incrementFaceCounter()
        
        # # Get the index value in the obja file
        # indexObja = self.faceTable.getObjaInd(indexModel)
        
        # Add the operation into the operation list
        self.operations.append(('f',indexModel, value))
        
        return None
    
    def operation_edit_vertex(self,indexModel:int,newValue:list):
        
        # # Get the corresponding index
        # indexObja = self.pointTable.getObjaInd(indexModel)
        
        # Add the opertaion into the operation list
        self.operations.append(('ev',indexModel,newValue))
    
    def operation_edit_face(self, indexModel:int,newValue:Face):
        
        # # Get the corresponding index
        # indexObja = self.faceTable.getObjaInd(indexModel)
        
        # Add the operation into the operation list
        self.operations.append(('ef',indexModel,newValue))
        
    def operation_change_color_faces(self,color:list):
        self.operations.append(('color',0,color))
        
    def __faceIndexModel_2_faceObjaModel(self,face:Face):
        
        a = self.pointTable.getObjaInd(face.a)
        b = self.pointTable.getObjaInd(face.b)
        c = self.pointTable.getObjaInd(face.c)
        
        return [a,b,c]
        
        
    def __add_vertex_output(self,indexModel:int, vertex:list):
        
        # First we need to create a link in the transcription table
        self.pointTable.addLink(indexModel,self.pointCounter)
        
        # We increment the pointCounter variable as this index is already taken
        self.incrementPointCounter()
        
        print('v {} {} {}'.format(vertex[0], vertex[1], vertex[2]), file=self.outputFile)
        
    def __add_face_output(self,indexModel:int,face:Face,color:list=None):
        
        # First we need to create a link in the transcription table
        self.faceTable.addLink(indexModel,self.faceCounter)
        
        # We increment the faceCounter variable as this index is already taken
        self.incrementFaceCounter()
        
        # Get the index value in the obja file
        indexObja = self.faceTable.getObjaInd(indexModel)
        
        print(indexModel)
        print(self.pointTable)
        print(self.faceTable)
        print(face)
        # First, in the face, it's the index of the model. We need to convert thoses index into obja index
        pointFaceObja = self.__faceIndexModel_2_faceObjaModel(face)
        
        # The add the face into the output file
        print('f {} {} {}'.format(pointFaceObja[0], pointFaceObja[1], pointFaceObja[2]), file=self.outputFile)
        
        # Add color to the face
        if color != None:
            print('fc {} {} {} {}'.format(indexObja+1,color[0],color[1],color[2]),file=self.outputFile)
                    
    def __edit_vertex_ouput(self,indexModel:int,vertex:list):
        
        # Get the corresponding index
        indexObja = self.pointTable.getObjaInd(indexModel)
        
        print('ev {} {} {} {}'.format(indexObja+1,vertex[0], vertex[1], vertex[2]), file=self.outputFile)
        
    def __edit_face_output(self,indexModel:int,face:Face,color:list=None):
        
        # Get the corresponding index
        indexObja = self.faceTable.getObjaInd(indexModel)
        
        # First, in the face, it's the index of the model. We need to convert thoses index into obja index
        pointFaceObja = self.__faceIndexModel_2_faceObjaModel(self,face)
        
        # The add the face into the output file
        print('ef {} {} {} {}'.format(indexObja+1,pointFaceObja[0], pointFaceObja[1], pointFaceObja[2]), file=self.outputFile)
        
        # Add color to the face
        if color != None:
            print('fc {} {} {} {}'.format(indexObja+1,color[0],color[1],color[2]),file=self.outputFile)
        
        
    def write_output(self):
        
        print("Start writing the output file \n")
        
        # Now defind a color for the faces
        color = [random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1)]
        
        # Then, reverse the operations list
        reverseOperations = self.operations[::-1]
        
        with open(self.outputFile+'a', 'w') as self.outputFile:
        
            # Finally, add all the link in the output file
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
        
    # First read the cube.obj file
    model = parse_file('example/suzanne.obj')
        
    # Create a writter
    writer = Writter('example/prout.obj',len(model.vertices),len(model.faces))
         
    # Add the points and the faces into the operation list
    for (indexModel,face) in enumerate(model.faces):
        writer.operation_add_face(indexModel,face)
        
    for (indexModel,vertice) in enumerate(model.vertices):
        writer.operation_add_vertex(indexModel,vertice)
        
    # Finally write into the output file
    writer.write_output()
    
    print('Test successfuly done')   
    
if __name__ == '__main__':
    print("Main")
    main()