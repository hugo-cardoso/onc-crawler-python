import requests, os
from xml.etree import ElementTree as Et
from airport import Airport, AirportChart

class DeceaApiService:
    api_url = 'http://aisweb.decea.gov.br/api'
    api_key = os.environ.get('API_DECEA_KEY')
    api_pass = os.environ.get('API_DECEA_PASS')
    
    def get_airport(self, icao_code:str):
        response = requests.get(self.api_url, params={
            'apiKey': self.api_key,
            'apiPass': self.api_pass,
            'area': 'rotaer',
            'icaoCode': icao_code,
        })

        try:
            document = Et.fromstring(response.text)
            
            if document.find('AeroCode') is not None:
                airport = Airport(icao_code)
                
                airportName = document.find('name')
                if airportName is not None:
                    airport.set_name(airportName.text.strip())
                
                return airport
        except:
            return None
        
    def get_airport_charts(self, icao_code:str):
        """Get a charts of a airport by ICAO code"""
    
        response = requests.get(self.api_url, params={
            'apiKey': self.api_key,
            'apiPass': self.api_pass,
            'area': 'cartas',
            'icaoCode': icao_code,
        })

        document = Et.fromstring(response.text)
        charts_items = document.find('cartas').findall('item')
        charts: list[AirportChart] = []

        for chart_item in charts_items:
            chart = AirportChart(chart_item.find('id').text)
            
            chart_name = chart_item.find('nome')
            if chart_name is not None:
                chart.set_name(chart_name.text.strip())
            
            charts.append(chart)

        return charts
    
    def get_airports_icao_list(self, page_number:int):
        items_per_page = 100
        
        response = requests.get(self.api_url, params={
            'apiKey': self.api_key,
            'apiPass': self.api_pass,
            'area': 'rotaer',
            'rowstart': str((page_number - 1) * items_per_page),
            'rowend': str(items_per_page),
            'type': 'AD'
        })

        document = Et.fromstring(response.text)
        airports = document.find('rotaer').findall('item')
        icao_codes: list[str] = []

        for airport in airports:
            icao_codes.append(airport.find('AeroCode').text)

        return icao_codes
    
    def get_airports_count(self):
        response = requests.get(self.api_url, params={
            'apiKey': self.api_key,
            'apiPass': self.api_pass,
            'area': 'rotaer',
            'rowend': '1',
            'type': 'AD'
        })

        document = Et.fromstring(response.text)
        count = document.find('rotaer').attrib['total']

        return int(count)
    
    def get_airports_pages_count(self):
        count = self.get_airports_count()
        items_per_page = 100
        return int(count / items_per_page)