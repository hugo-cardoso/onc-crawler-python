import json, os, concurrent.futures
from decea_api import *

def airport_logger(airport:Airport):
    def create_brackets(value:str):
        return "[" + value + "]"
    
    print(create_brackets(airport.icao_code) + " - " + airport.name + " " + create_brackets(str(len(airport.chart_list))))

def find_airport(icao_code):
    airport = get_airport(icao_code)
    
    if airport is None:
        return None

    airport.set_chart_list(get_airport_charts(icao_code))
    
    if not os.path.exists('airports'):
        os.makedirs('airports')
    
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

    airport_logger(airport)

pages_count = get_airports_pages_count()

for page in range(1, (pages_count + 1)):
    print('Start page:', str(page) + "/" + str(pages_count))
    airports_icao_list = get_airports_icao_list(page)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(find_airport, icao_code) for icao_code in airports_icao_list]
    print('End page:', page)
