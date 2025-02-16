import os
import time
import torch
import polars as pl
from app.crosscutting.aws_s3_client import AwsS3Client


class NewsRecommendationRepository:

    MODEL_CACHE = {}
    DATA_CACHE = {}
    BUCKET_NAME = os.getenv("BUCKET_NAME")

    def __init__(self, client: AwsS3Client):
        self.client = client

    def get_pytorch_model(self, name, identifier):
        start_time = time.time()
        full_name = f"{name}-{identifier}"

        if full_name in self.MODEL_CACHE:
            return self.MODEL_CACHE[full_name]

        model_serialized = self.client.get_object_body_as_bytes_io(self.BUCKET_NAME, f"models/{full_name}.pth")
        model = torch.jit.load(model_serialized)
        self.MODEL_CACHE[full_name] = model
        print(f"Model '{full_name}' downloaded and deserialized in: {(time.time() - start_time) * 1000:.2f} ms")
        return model

    def get_news_data(self, identifier: str):
        start_time = time.time()
        full_name = f"news_data-{identifier}"

        if full_name in self.DATA_CACHE:
            return self.DATA_CACHE[full_name]

        data = self.client.get_parquet_object_as_polars_df(self.BUCKET_NAME, f"models/data-betelgeuse/{full_name}.parquet")
        self.DATA_CACHE[full_name] = data
        print(f"News data file '{full_name}.parquet' downloaded and read in: {(time.time() - start_time) * 1000:.2f} ms")
        return data

    def get_similarity_matrix(self, identifier: str):
        start_time = time.time()
        full_name = f"similarity_matrix-{identifier}"

        if full_name in self.DATA_CACHE:
            return self.DATA_CACHE[full_name]

        data = self.client.get_parquet_object_as_polars_df(self.BUCKET_NAME, f"models/data-betelgeuse/{full_name}.parquet")
        self.DATA_CACHE[full_name] = data
        print(f"News similarity matrix '{full_name}.parquet' downloaded and read in: {(time.time() - start_time) * 1000:.2f} ms")
        return data

    def get_feature_weights(self, identifier: str):
        start_time = time.time()
        full_name = f"feature_weights-{identifier}"

        if full_name in self.DATA_CACHE:
            return self.DATA_CACHE[full_name]

        data = self.client.get_parquet_object_as_polars_df(self.BUCKET_NAME, f"models/data-betelgeuse/{full_name}.parquet")
        self.DATA_CACHE[full_name] = data
        print(f"Feature weights file '{full_name}.parquet' downloaded and read in: {(time.time() - start_time) * 1000:.2f} ms")
        return data