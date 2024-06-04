import os
from services.airport_chart_service import AirportChartService
from models.airport import Airport
from pymongo import MongoClient

class AirportsRepository:
    mongo_client = MongoClient(os.environ.get('DB_CONNECTION_STRING'))
    airports_collection = mongo_client['onc']['airports']
    airports_charts_s3_service = AirportChartService()
    
    def __create_airport_object(self, airport:Airport):
        return {
            '_id': airport.icao_code,
            'icao_code': airport.icao_code,
            'name': airport.name,
            'location': {
                'city': airport.location.city,
                'state_or_province': airport.location.state_or_province,
                'country': 'Brazil',
                'lat': airport.location.lat,
                'lng': airport.location.lng
            },
            'chart_list': [
                {
                    'id': chart.id,
                    'name': chart.name
                }
                for chart in airport.chart_list
            ],
            'runway_list': [
                {
                    'ident': runway.ident,
                    'width': runway.width,
                    'length': runway.length
                }
                for runway in airport.runway_list
            ]
        }
  
    def find_by_icao(self, icao_code:str):
        return self.airports_collection.find_one({'_id': icao_code})
    
    def create(self, airport:Airport):
        self.airports_collection.insert_one(self.__create_airport_object(airport))
            
    def update(self, airport:Airport):
        self.airports_collection.update_one({'_id': airport.icao_code}, {'$set': self.__create_airport_object(airport)})
  
    def create_or_update(self, airport:Airport):
        airport_saved = self.find_by_icao(airport.icao_code)
            
        self.airports_charts_s3_service.save_charts(airport.icao_code, airport.chart_list)
        
        if airport_saved is None:
            self.create(airport)
        else:
            self.update(airport)