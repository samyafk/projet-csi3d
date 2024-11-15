from obja import *
from log import *
from writer import *

class Compresser(object):

    def __init__(self, filename:str):
        
        # Creation of the var model and parse file
        self.__model = Model()
        self.__model.parse_file('example/'+filename)
        
        # Creation of the logger
        self.__logger = Logger()
        
        # Creation of the writter
        nbrOfVertices = len(self.__model.vertices)
        nbrOfFaces = len(self.__model.faces)
        self.writer = Writer('example/'+filename, nbrOfVertices, nbrOfFaces, self.__logger)
        
        
        
        
    