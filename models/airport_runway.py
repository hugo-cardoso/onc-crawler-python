class AirportRunway:
    width:int
    length:int
    
    def __init__(self, ident:str):
        self.ident = ident
        
    def set_width(self, width:str):
        self.width = width
        return self
    
    def set_length(self, length:str):
        self.length = length
        return self