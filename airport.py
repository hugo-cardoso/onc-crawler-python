from airport_chart import AirportChart

class Airport:
    name:str
    chart_list: list[AirportChart]
  
    def __init__(self, icao_code:str):
        self.icao_code = icao_code
        
    def set_name(self, name:str):
        self.name = name
        return self
    
    def set_chart_list(self, chart_list:list[AirportChart]):
        self.chart_list = chart_list
        return self