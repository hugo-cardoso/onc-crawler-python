class AirportChart:
    name:str
    
    def __init__(self, id:str):
        self.id = id
        
    def set_name(self, name:str):
        self.name = name
        return self