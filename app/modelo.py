from pydantic import BaseModel

# Define a classe para entrada de dados no modelo
class InputData(BaseModel):

    # Tipagem dos dados
    Area: float
    Garage: int
    FirePlace: int
    Baths: int
    White_Marble: int
    Black_Marble: int
    Indian_Marble: int
    Floors: int
    City: int
    Solar: int
    Electric: int
    Fiber: int
    Glass_Doors: int
    Swiming_Pool: int
    Garden: int
    
    

