import requests
import concurrent.futures
from xml.etree import ElementTree as Et

def get_airport(icao_code):
    response = requests.get('http://aisweb.decea.gov.br/api', params={
        'apiKey': '1635529713',
        'apiPass': '2f7dfb3c-90cf-11eb-9a71-0050569ac1e0',
        'area': 'rotaer',
        'icaoCode': icao_code,
    })

    try:
        document = Et.fromstring(response.text)
        if document.find('AeroCode') is not None:
            return document
    except:
        return None

def get_airport_charts(icao_code):
    response = requests.get('http://aisweb.decea.gov.br/api', params={
        'apiKey': '1635529713',
        'apiPass': '2f7dfb3c-90cf-11eb-9a71-0050569ac1e0',
        'area': 'cartas',
        'icaoCode': icao_code,
    })

    document = Et.fromstring(response.text)
    charts = document.find('cartas').findall('item')
    chart_ids = []

    for chart in charts:
        chart_ids.append(chart.find('id').text)

    return chart_ids

def get_airports_list(page_number:int):
    items_per_page = 100
    
    response = requests.get('http://aisweb.decea.gov.br/api', params={
        'apiKey': '1635529713',
        'apiPass': '2f7dfb3c-90cf-11eb-9a71-0050569ac1e0',
        'area': 'rotaer',
        'rowstart': str((page_number - 1) * items_per_page),
        'rowend': str(page_number * items_per_page),
        'type': 'AD'
    })

    document = Et.fromstring(response.text)
    airports = document.find('rotaer').findall('item')
    icao_codes = []

    for airport in airports:
        icao_codes.append(airport.find('AeroCode').text)

    return icao_codes

def get_airports_count():    
    response = requests.get('http://aisweb.decea.gov.br/api', params={
        'apiKey': '1635529713',
        'apiPass': '2f7dfb3c-90cf-11eb-9a71-0050569ac1e0',
        'area': 'rotaer',
        'rowend': '1',
        'type': 'AD'
    })

    document = Et.fromstring(response.text)
    count = document.find('rotaer').attrib['total']

    return int(count)

def get_airports_pages_count():
    count = get_airports_count()
    items_per_page = 100
    return int(count / items_per_page)

def find_airport(icao_code):
    airport = get_airport(icao_code)
    if airport is None:
        return None
    
    airportCharts = get_airport_charts(icao_code)

    airportIcao = airport.find('AeroCode')
    if airportIcao is not None:
        airportIcao = airportIcao.text.strip()

    airportName = airport.find('name')
    if airportName is not None:
        airportName = airportName.text.strip()

    print(airportIcao + " - " + airportName + "[" + str(len(airportCharts)) + "]")

# pages_count = get_airports_pages_count()
pages_count = 3

for page in range(1, (pages_count + 1)):
    print('Start page:', str(page) + "/" + str(pages_count))
    airports_list = get_airports_list(page)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(find_airport, icao_code) for icao_code in airports_list]
    print('End page:', page)

# while page <= page_limit:
#     airports_list = get_airports_list(page)
#     with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#         futures = [executor.submit(find_airport, icao_code) for icao_code in airports_list]
#     page += 1

# airports_list = get_airports_list(1)

# with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#     futures = [executor.submit(find_airport, icao_code) for icao_code in airports_list]
