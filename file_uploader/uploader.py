import os
import json
import boto3
from google.cloud import storage
from google.oauth2 import service_account

class FileUploader:
    def __init__(self, config):
        self.s3_bucket = config['s3_bucket']
        self.gcs_bucket = config['gcs_bucket']
        self.s3_file_types = config['s3_file_types']
        self.gcs_file_types = config['gcs_file_types']
        self.directory = config['directory']

        # AWS S3 Client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key']
        )

        # Google Cloud Storage Client
        credentials = service_account.Credentials.from_service_account_file(
            config['gcp_credentials_file']
        )
        self.gcs_client = storage.Client(
            project=config['gcp_project_id'],
            credentials=credentials
        )

    def upload_to_s3(self, file_path):
        bucket_name = self.s3_bucket
        file_name = os.path.basename(file_path)
        self.s3_client.upload_file(file_path, bucket_name, file_name)
        print(f"Uploaded {file_name} to S3 bucket {bucket_name}")

    def upload_to_gcs(self, file_path):
        bucket_name = self.gcs_bucket
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(os.path.basename(file_path))
        blob.upload_from_filename(file_path)
        print(f"Uploaded {file_path} to GCS bucket {bucket_name}")

    def process_files(self):
        for root, _, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.lower().endswith(tuple(self.s3_file_types)):
                    self.upload_to_s3(file_path)
                elif file.lower().endswith(tuple(self.gcs_file_types)):
                    self.upload_to_gcs(file_path)
