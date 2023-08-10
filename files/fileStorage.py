# standard
import os

# third-party
import boto3


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class UnionStorage:
    def __init__(self):
        self.client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('BUCKETEER_AWS_REGION')
        )
        self.bucket_name = os.environ.get('BUCKETEER_BUCKET_NAME')

    def get_file(self, file_type: str, file_name: str):
        file = self.client.get_object(
            Bucket=self.bucket_name,
            Key=f'{file_type}.{file_name}'
        )
        return file
