import os, concurrent.futures
from decea_api_service import *
from airports_repository import *
from airport import *

class Crawler:
    decea_api_service = DeceaApiService()
    airports_repository = AirportsRepository()
    pages_count = decea_api_service.get_airports_pages_count()
    
    def __page_logger(self, text:str, page:int):
        print(text, str(page) + "/" + str(self.pages_count))
    
    def __airport_logger(self, airport:Airport):
        def create_brackets(value:str):
            return "[" + value + "]"
        
        print(create_brackets(airport.icao_code) + " - " + airport.name + " " + create_brackets(str(len(airport.chart_list))))
        
    def find_airport(self, icao_code:str):
        airport = self.decea_api_service.get_airport(icao_code)
        
        if airport is None:
            return None
        
        airport_charts = self.decea_api_service.get_airport_charts(icao_code)
        airport.set_chart_list(airport_charts)
        
        self.airports_repository.create(airport)
        self.__airport_logger(airport)
        
    def init(self):
        workers_count = int(os.environ.get('WORKERS_COUNT'))
        
        print('Start crawler with: ' + str(workers_count) + ' workers')
        
        for page in range(1, (self.pages_count + 1)):
            self.__page_logger('Start page:', page)
            airports_icao_list = self.decea_api_service.get_airports_icao_list(page)
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers_count) as executor:
                futures = [executor.submit(self.find_airport, icao_code) for icao_code in airports_icao_list]
            self.__page_logger('End page:', page)

crawler = Crawler()
crawler.init()
