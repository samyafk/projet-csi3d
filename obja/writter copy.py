from transcriptionTable import *
from obja import *
import random
from tqdm import tqdm


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
        
        # First we need to create a link in the transcription table
        self.pointTable.addLink(indexModel,self.pointCounter)
        
        # We increment the pointCounter variable as this index is already taken
        self.incrementPointCounter()
        
        # Get the index value in the obja file
        indexObja = self.pointTable.getObjaInd(indexModel)
        
        # Add the operation into the operation list
        self.operations.append(('v',indexObja, value))
    
    def operation_add_face(self,indexModel:int,value:Face):
        
        # First we need to create a link in the transcription table
        self.faceTable.addLink(indexModel,self.faceCounter)
        
        # We increment the pointCounter variable as this index is already taken
        self.incrementFaceCounter()
        
        # Get the index value in the obja file
        indexObja = self.faceTable.getObjaInd(indexModel)
        
        # Add the operation into the operation list
        self.operations.append(('v',indexObja, value))
        
        return None
    
    def operation_edit_vertex(self,indexModel:int,newValue:list):
        
        # Get the corresponding index
        indexObja = self.pointTable.getObjaInd(indexModel)
        
        # Add the opertaion into the operation list
        self.operations.append(('ev',indexObja,newValue))
    
    def operation_edit_face(self, indexModel:int,newValue:Face):
        
        # Get the corresponding index
        indexObja = self.faceTable.getObjaInd(indexModel)
        
        # Add the operation into the operation list
        self.operations.append(('ef',indexObja,newValue))
        
    def operation_change_color_faces(self):
        return None
        
    def __faceIndexModel_2_faceObjaModel(self,face:Face):
        
        a = self.pointTable.getObjaInd(face.a)
        b = self.pointTable.getObjaInd(face.b)
        c = self.pointTable.getObjaInd(face.c)
        
        return [a,b,c]
        
        
    def __add_vertex_output(self, vertex:list):
        print('v {} {} {}'.format(vertex[0], vertex[1], vertex[2]), file=self.outputFile)
        
    def __add_face_output(self,indexObja:int,face:Face,color:list=None):
        
        # First, in the face, it's the index of the model. We need to convert thoses index into obja index
        pointFaceObja = self.__faceIndexModel_2_faceObjaModel(self,face)
        
        # The add the face into the output file
        print('f {} {} {}'.format(pointFaceObja[0], pointFaceObja[1], pointFaceObja[2]), file=self.outputFile)
        
        # Add color to the face
        if color != None:
            print('fc {} {} {} {}'.format(indexObja+1,color[0],color[1],color[2],file=self.outputFile))
                    
    def __edit_vertex_ouput(self,indexObja:int,vertex:list):
        print('ev {} {} {} {}'.format(indexObja+1,vertex[0], vertex[1], vertex[2]), file=self.outputFile)
        
    def __edit_face_output(self,indexObja:int,face:Face,color:list=None):
        
        # First, in the face, it's the index of the model. We need to convert thoses index into obja index
        pointFaceObja = self.__faceIndexModel_2_faceObjaModel(self,face)
        
        # The add the face into the output file
        print('ef {} {} {} {}'.format(indexObja+1,pointFaceObja[0], pointFaceObja[1], pointFaceObja[2]), file=self.outputFile)
        
        # Add color to the face
        if color != None:
            print('fc {} {} {} {}'.format(indexObja+1,color[0],color[1],color[2],file=self.outputFile))
        
        
    def write_output(self):
        
        print("Start writing the output file \n")
        
        # First, check if the two table are bijective
        self.faceTable.isBijective()
        self.pointTable.isBijective()
        
        # Now defind a color for the faces
        color = [random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1)]
        
        # Then, reverse the operations list
        reverseOperations = self.operation[::-1]
        
        # Finally, add all the link in the output file
        for (ty, indexObja, value) in tqdm(reverseOperations):
            
            if ty == "v":
                self.__add_vertex_output(value)
            elif ty == "f":
                self.__add_face_output(indexObja, value,color)  
            elif ty == "ev":
                self.__edit_vertex_ouput(indexObja, value)
            elif ty == "ef":
                self.__edit_face_output(indexObja, value)        
            else:
                raise SyntaxError("Too understand the type")
            
        print("Ouput File sucesfully write !")
        
