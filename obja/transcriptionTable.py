import numpy as np

class ObjaNotFoundError(Exception):
    """Exception raised when a link between a model indice and an obja indice is not found"""

    def __init__(self, model_index, message="this model index does not correspond to any object index"):
        self.model_index = model_index
        self.message = f"{message}: {model_index}"
        super().__init__(self.message)
        
class ModelNotFoundError(Exception):
    """Exception raised when a link between a model indice and an obja indice is not found"""

    def __init__(self, obja_index, message="this obja index does not correspond to any model index"):
        self.obja_index = obja_index
        self.message = f"{message}: {obja_index}"
        super().__init__(self.message)
        
class TranscriptionTable(object):
    
    def __init__(self,name:str,nbrOfObject:int):
        self.name = name
        self.table = np.full(nbrOfObject, fill_value=None)
        
    def addLink(self,model:int,obja:int):
        
        if self.table[model] != None:
            print("Warning, a link is already added")
            
        self.table[model] = obja
        
    def getObjaInd(self,model:int):
        if self.table[model] == None:
            # Création d'une exception spéciale à raise
            raise ObjaNotFoundError(model)
        else:
            return self.table[model]
        
    def getModelInd(self, obja: int):
        
        # Find indices in the table that match the given obja value
        matching_indices = [index for index, value in enumerate(self.table) if value == obja]
        
        if len(matching_indices) == 0:
            # Raise the custom exception if no matching index is found
            raise ObjaNotFoundError(obja, "No model index corresponds to the provided object index")
        elif len(matching_indices) > 1:
            # Raise a ValueError if multiple indices match
            raise ValueError(f"Multiple model indices found for object index {obja}: {matching_indices}")
        else:
            # Return the single matching index
            return matching_indices[0]
        
    def isBijective(self):
        # To verify that each value is correlated ()
        #TODO
        
        return None
        
def main():
    
    # Creation of a table
    table = TranscriptionTable("Suzanne",5)
    
    #table.getModelInd(4)
    #table.getObjaInd(1)
    
    # The are five value. Let's add a link between the first index and a number 
    table.addLink(1,4)
    #table.addLink(2,4)
    print(table.getModelInd(4))
    
    
    


if __name__ == '__main__':
    main()