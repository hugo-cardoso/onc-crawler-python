class AirportLocation:
    state_or_province = ''
    city = ''
    lat:int
    lng:int
        
    def set_state_or_province(self, state_or_province:str):
        self.state_or_province = state_or_province
        return self

    def set_city(self, city:str):
        self.city = city
        return self
    
    def set_lat(self, lat:int):
        self.lat = lat
        return self
    
    def set_lng(self, lng:int):
        self.lng = lng
        return self