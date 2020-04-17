import os

import boto3

s3_client = boto3.client('s3')
bucket = os.environ['AWS_BUCKET']
aws_region = os.environ['AWS_REGION']

bucket_url = f'https://{bucket}.s3-{aws_region}.amazonaws.com'


def upload_fileobj_to_s3(key: str, fileobj) -> str:
    s3_client.upload_fileobj(fileobj, bucket, key)
    return f'{bucket_url}/{key}'


def download_fileobj_from_s3(key: str, output_path: str):
    with open(output_path, 'wb') as data:
        s3_client.download_fileobj(bucket, key, data)
