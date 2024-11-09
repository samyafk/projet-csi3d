import numpy as np

class ObjaNotFoundError(Exception):
    """Exception raised when a link between a model index and an obja index is not found."""

    def __init__(self, model_index, message="this model index does not correspond to any object index"):
        self.model_index = model_index
        self.message = f"{message}: {model_index}"
        super().__init__(self.message)

class ModelNotFoundError(Exception):
    """Exception raised when a link between a model index and an obja index is not found."""

    def __init__(self, obja_index, message="this obja index does not correspond to any model index"):
        self.obja_index = obja_index
        self.message = f"{message}: {obja_index}"
        super().__init__(self.message)

class TableNotBijectiveError(Exception):
    """Exception raised when the table is not bijective."""

    def __init__(self, table_name, message="The table is not bijective"):
        self.table_name = table_name
        self.message = f"{message}: {table_name}"
        super().__init__(self.message)

class TranscriptionTable(object):
    
    def __init__(self, name: str, nbrOfObject: int):
        self.name = name
        self.table = np.full(nbrOfObject, fill_value=None)
        
    def addLink(self, model: int, obja: int):
        if self.table[model] is not None:
            print("Warning, a link is already added")
        self.table[model] = obja
        
    def getObjaInd(self, model: int):
        if self.table[model] is None:
            raise ObjaNotFoundError(model)
        else:
            return self.table[model]
        
    def getModelInd(self, obja: int):
        matching_indices = [index for index, value in enumerate(self.table) if value == obja]
        if len(matching_indices) == 0:
            raise ObjaNotFoundError(obja, "No model index corresponds to the provided object index")
        elif len(matching_indices) > 1:
            raise ValueError(f"Multiple model indices found for object index {obja}: {matching_indices}")
        else:
            return matching_indices[0]
        
    def isBijective(self):
        # Check if there are any None values, which means the bijection is incomplete
        if None in self.table:
            raise TableNotBijectiveError(self.name, "Table contains None values and is incomplete")
        
        # Check for uniqueness by converting the table to a set and comparing lengths
        if len(set(self.table)) != len(self.table):
            raise TableNotBijectiveError(self.name, "Table has duplicate obja values and is not bijective")
        
        print(f"The table '{self.name}' is bijective.")

def main():
    table = TranscriptionTable("Suzanne", 5)
    
    # Add links
    table.addLink(0, 2)
    table.addLink(1, 3)
    table.addLink(2, 1)
    table.addLink(3, 4)
    table.addLink(4, 0)
    
    # Check bijectivity
    try:
        table.isBijective()  # Expected: The table "Suzanne" is bijective.
    except TableNotBijectiveError as e:
        print(e)

    # Add a duplicate to test non-bijective
    table.addLink(1, 4)
    try:
        table.isBijective()  # Expected: TableNotBijectiveError
    except TableNotBijectiveError as e:
        print(e)

if __name__ == '__main__':
    main()
