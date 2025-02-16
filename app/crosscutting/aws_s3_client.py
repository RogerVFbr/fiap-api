import boto3
import io
import polars as pl


class AwsS3Client:

    def __init__(self):
        self.client = boto3.resource('s3')

    def get_object_body_as_bytes_io(self, bucket_name, object_name):
        obj = self.client.Object(bucket_name, object_name)
        return io.BytesIO(obj.get()['Body'].read())

    def get_parquet_object_as_polars_df(self, bucket_name, object_name):
        bytes_io = self.get_object_body_as_bytes_io(bucket_name, object_name)
        return pl.read_parquet(bytes_io)