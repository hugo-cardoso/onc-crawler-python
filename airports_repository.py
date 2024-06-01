import os, json
from airport import Airport

class AirportsRepository:
  def __init__(self):
    if not os.path.exists('airports'):
        os.makedirs('airports')
  
  def create(self, airport:Airport):
    with open("airports/" + airport.icao_code + '.json', 'w', encoding='utf-8') as f:
        json.dump({
            'icao_code': airport.icao_code,
            'name': airport.name,
            'chart_list': [
                {
                    'id': chart.id,
                    'name': chart.name
                }
                for chart in airport.chart_list
            ]
        }, f, ensure_ascii=False, indent=4)
    