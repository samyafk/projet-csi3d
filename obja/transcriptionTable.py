import numpy as np

class ObjaNotFoundError(Exception):
    def __init__(self, model_index, message="this model index does not correspond to any object index"):
        self.model_index = model_index
        self.message = f"{message}: {model_index}"
        super().__init__(self.message)

class ModelNotFoundError(Exception):
    def __init__(self, obja_index, message="this obja index does not correspond to any model index"):
        self.obja_index = obja_index
        self.message = f"{message}: {obja_index}"
        super().__init__(self.message)

class TableNotBijectiveError(Exception):
    def __init__(self, table_name, message="The table is not bijective"):
        self.table_name = table_name
        self.message = f"{message}: {table_name}"
        super().__init__(self.message)

class TranscriptionTable(object):
    
    def __init__(self, name: str, nbrOfObject: int):
        self.name = name
        self.table = np.full(nbrOfObject, fill_value=None)
        
    def __repr__(self) -> str:
        return f"TranscriptionTable(name={self.name}, table={self.table})"
        
    def addLink(self, model_idx: int, obja_idx: int) -> None:
        """Add a link between a model index and an obja index.
        
        Args:
            model_idx (int): the model index
            obja_idx (int): the obja index
        """
        
        
        if self.table[model_idx] is not None:
            print("Warning, a link is already added")
            
        self.table[model_idx] = obja_idx
        
    def getObjaInd(self, model_idx: int) -> int:
        """Get the obja index corresponding to a model index.
        
        Args:
            model_idx (int): the model index
            
        Returns:
            int: the obja index
        """
        obja_link = self.table[model_idx]
        
        if obja_link is None:
            raise ObjaNotFoundError(model_idx)
        else:
            return obja_link
        
    def getModelInd(self, obja_idx: int) -> int:
        """Get the model index corresponding to an obja index.
        
        Args:
            obja_idx (int): the obja index
            
        Returns:
            int: the model index
        """
        matching_indices = [index for index, value in enumerate(self.table) if value == obja_idx]
        
        if len(matching_indices) == 0:
            raise ModelNotFoundError(obja_idx, "No model index corresponds to the provided object index")
        elif len(matching_indices) > 1:
            raise ValueError(f"Multiple model indices found for object index {obja_idx}: {matching_indices}")
        else:
            return matching_indices[0]
        
    def isBijective(self) -> None:
        """Check if the table is bijective."""
        
        is_not_complete = None in self.table
        
        if is_not_complete:
            raise TableNotBijectiveError(self.name, "Table contains None values and is incomplete")
        
        has_duplicates = len(set(self.table)) != len(self.table)
        
        if has_duplicates:
            raise TableNotBijectiveError(self.name, "Table has duplicate obja values and is not bijective")
        
        print(f"The table '{self.name}' is bijective.")
        
    def len(self) -> int:
        """Return the length of the table."""
        return len(self.table)
    
    def getNumberOfUndefinedLink(self) -> int:
        """Return the number of undefined links in the table.
        
        Returns:
            int: the number of undefined links
        """
        return np.sum([1 for item in self.table if item is None])

def main():
    table = TranscriptionTable("Suzanne", 5)
    
    table.addLink(0, 2)
    table.addLink(1, 3)
    table.addLink(2, 1)
    table.addLink(3, 4)
    table.addLink(4, 0)
    
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
