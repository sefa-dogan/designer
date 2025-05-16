from typing import List,TypedDict

class GraphState(TypedDict):
    """
    
    Represents the state of a graph
    Attributes:
        encoded_raw_image: raw image as base64 format
        encoded_processed_image: processed image as base64 format
        items: list of items
        correct_design: is processed image sense or not
        
    """
    encoded_raw_image:str
    encoded_processed_image: str
    items:List[str]
    correct_design:bool