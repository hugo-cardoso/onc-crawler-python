import os, json
from airport import Airport

class AirportsRepository:
    def __init__(self):
        if not os.path.exists('airports'):
            os.makedirs('airports')
    
    @staticmethod
    def prepare():
        for file in os.listdir('airports'):
            os.remove('airports/' + file)
  
    def create(self, airport:Airport):
        with open("airports/" + airport.icao_code + '.json', 'w', encoding='utf-8') as f:
            json.dump({
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
            }, f, ensure_ascii=False, indent=4)
    