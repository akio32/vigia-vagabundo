import logging
import boto3
from botocore.exceptions import ClientError
import os

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    # Create a session using the specified configuration file
    session = boto3.Session(profile_name='default')
    s3_client = session.client('s3')

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


file_name = r'C:\Users\andre\Desktop\coding\git\vigia-vagabundo\teste.csv'
bucket = "vigiavagabundo"
object_name = "propostas/teste"

result = upload_file(file_name=file_name, bucket=bucket, object_name=object_name)