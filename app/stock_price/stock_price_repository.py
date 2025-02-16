import os
import torch

from app.crosscutting.aws_s3_client import AwsS3Client


class StockPriceRepository:

    DATA = {}
    BUCKET_NAME = os.getenv("BUCKET_NAME")

    def __init__(self, client: AwsS3Client):
        self.client = client

    def get_model(self, name, identifier):
        full_name = f"{name}-{identifier}"

        if full_name in self.DATA:
            return self.DATA[full_name]

        model_serialized = self.client.get_object_body_as_bytes_io(self.BUCKET_NAME, f"models/{full_name}.pth")
        model = torch.jit.load(model_serialized)
        self.DATA[full_name] = model
        return self.DATA[full_name]