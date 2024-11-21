import boto3
import io


class AwsS3Client:

    def __init__(self):
        self.client = boto3.resource('s3')

    def get_object_body_as_bytes(self, bucket_name, object_name):
        obj = self.client.Object(bucket_name, object_name)
        return io.BytesIO(obj.get()['Body'].read())