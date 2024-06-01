import os, requests, boto3
from airport import AirportChart
from io import BytesIO
from botocore.exceptions import ClientError

class AirportsChartsS3Repository:
    bucket_name = 'onc-charts'
    s3_client = boto3.client(
        service_name='s3',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
    )
    
    def __create_chart_url(self, chart_id:str):
        return f'https://aisweb.decea.gov.br/download/?arquivo={chart_id}&apikey={os.environ.get("API_DECEA_KEY")}.pdf'
    
    def __check_file_exists(self, object_name:str):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=object_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise
            
    def upload_chart(self, icao_code:str, chart:AirportChart):
        file_name = f'{icao_code.upper()}/{chart.id}.pdf'
        
        if self.__check_file_exists(file_name):
            return
        
        response = requests.get(self.__create_chart_url(chart.id), stream=True)
        response.raise_for_status()
        
        chart_stream = BytesIO(response.content)
        
        self.s3_client.upload_fileobj(
            chart_stream,
            self.bucket_name,
            file_name
        )