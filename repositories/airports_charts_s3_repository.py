import os, boto3
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
    
    def check_file_exists(self, object_name:str):
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=object_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise
            
    def upload_chart(self, file_name:str, file_content: bytes):
        chart_stream = BytesIO(file_content)
        
        self.s3_client.upload_fileobj(
            chart_stream,
            self.bucket_name,
            file_name
        )