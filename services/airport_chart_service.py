import os, requests
from io import BytesIO

from repositories.airports_charts_s3_repository import AirportsChartsS3Repository
from models.airport_chart import AirportChart

class AirportChartService:
    s3_repository = AirportsChartsS3Repository()
  
    def __create_chart_url(self, chart_id:str):
        return f'https://aisweb.decea.gov.br/download/?arquivo={chart_id}&apikey={os.environ.get("API_DECEA_KEY")}.pdf'
    
    def __create_chart_path(self, icao_code:str, chart_id:str):
        return f'{icao_code.upper()}/{chart_id}.pdf'
  
    def save_chart(self, icao_code:str, chart:AirportChart):
        file_name = self.__create_chart_path(icao_code, chart.id)
        
        if self.s3_repository.check_file_exists(file_name):
            return
        
        response = requests.get(self.__create_chart_url(chart.id), stream=True)
        response.raise_for_status()
        
        chart_stream = BytesIO(response.content)
        
        self.s3_repository.upload_file(file_name, chart_stream)
        
    def save_charts(self, icao_code:str, chart_list:list[AirportChart]):
        try:
            saved_chart_ids:list[str] = [file_name.removesuffix('.pdf') for file_name in self.s3_repository.get_files(icao_code)]
            updated_chart_ids = [chart.id for chart in chart_list]
            
            charts_ids_to_save = set(updated_chart_ids) - set(saved_chart_ids)
            charts_ids_to_delete = set(saved_chart_ids) - set(updated_chart_ids)
            
            for chart_id in charts_ids_to_save:
                self.save_chart(icao_code, AirportChart(chart_id))
                
            for chart_id in charts_ids_to_delete:
                self.s3_repository.delete_file(self.__create_chart_path(icao_code, chart_id))
        except Exception as e:
            print(f'Error on save_charts: {e}')