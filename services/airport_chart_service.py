import os, requests
from io import BytesIO

from repositories.airports_charts_s3_repository import AirportsChartsS3Repository
from models.airport_chart import AirportChart
from models.airport import AirportChart

class AirportChartService:
    s3_repository = AirportsChartsS3Repository()
  
    def __create_chart_url(self, chart_id:str):
        return f'https://aisweb.decea.gov.br/download/?arquivo={chart_id}&apikey={os.environ.get("API_DECEA_KEY")}.pdf'
  
    def save_chart(self, icao_code:str, chart:AirportChart):
        file_name = f'{icao_code.upper()}/{chart.id}.pdf'
        
        if self.s3_repository.check_file_exists(file_name):
            return
        
        response = requests.get(self.__create_chart_url(chart.id), stream=True)
        response.raise_for_status()
        
        chart_stream = BytesIO(response.content)
        
        self.s3_repository.upload_chart(chart_stream, file_name)
  