from airport_chart import AirportChart
from airport_runway import AirportRunway
from airport_location import AirportLocation

class Airport:
    name:str
    location: AirportLocation
    chart_list: list[AirportChart]
    runway_list: list[AirportRunway]
  
    def __init__(self, icao_code:str):
        self.icao_code = icao_code
        
    def set_name(self, name:str):
        self.name = name
        return self
    
    def set_location(self, location:AirportLocation):
        self.location = location
        return self
    
    def set_chart_list(self, chart_list:list[AirportChart]):
        self.chart_list = chart_list
        return self
    
    def set_runway_list(self, runway_list:list[AirportRunway]):
        self.runway_list = runway_list
        return self