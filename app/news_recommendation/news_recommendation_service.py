import torch
import numpy as np
import polars as pl
from sklearn.preprocessing import MinMaxScaler

from app.news_recommendation.news_recommendation_repository import NewsRecommendationRepository


class NewsRecommendationService:

    SCALER = MinMaxScaler()

    def __init__(self, repo: NewsRecommendationRepository):
        self.repo = repo

    def infer(self, model_name, model_id, user_id: str, views: dict) -> list[str]:
        predicted_clusters = self.__predict_clusters(model_name, model_id, user_id, pl.DataFrame(views))
        return self.__get_target_news_ids(model_id, predicted_clusters)

    def __predict_clusters(self,
                           model_name: str,
                           model_id: str,
                           user_id: str,
                           views: pl.DataFrame):

        model = self.repo.get_pytorch_model(model_name, model_id)
        news_data = self.repo.get_news_data(model_id)
        similarity_matrix = self.repo.get_similarity_matrix(model_id).transpose().to_dict()
        feature_weights = self.repo.get_feature_weights(model_id).to_dict()

        return (
            views.lazy()
            .select(
                pl.lit(user_id).alias('user_id'),
                pl.col('news_id'),
                pl.col('scroll_percentage'),
                pl.col('time_on_page'),
                pl.col('viewed_at').map_elements(lambda x: x.timestamp(), return_dtype=pl.Float64).alias('viewed_at_timestamp'),
            )
            .join(
                news_data.lazy(),
                left_on='news_id', right_on='page', how='left'
            )
            # Scale metrics
            .with_columns(
                ((pl.col("scroll_percentage") - pl.col("scroll_percentage").min()) / (pl.col("scroll_percentage").max() - pl.col("scroll_percentage").min())).alias("scroll_percentage_scaled"),
                ((pl.col("time_on_page") - pl.col("time_on_page").min()) / (pl.col("time_on_page").max() - pl.col("time_on_page").min())).alias("time_on_page_scaled"),
                ((pl.col("viewed_at_timestamp") - pl.col("viewed_at_timestamp").min()) / (pl.col("viewed_at_timestamp").max() - pl.col("viewed_at_timestamp").min())).alias("viewed_at_scaled"),
            )
            # Build feature index
            .with_columns(
                pl.struct(pl.col("scroll_percentage_scaled"), pl.col("time_on_page_scaled"), pl.col("viewed_at_scaled")).map_elements(lambda x: self.__build_features_index(x, feature_weights), return_dtype=pl.Float32).alias("features_index"),
            )
            # Populate feature columns
            .with_columns(
                [pl.when(pl.col("cluster") == x).then(pl.col('features_index')).otherwise(0).alias(f"cluster_{x}") for x in range(len(similarity_matrix))]
            )
            # Coalesce feature columns
            .group_by(
                'cluster'
            )
            .agg(
                [pl.col('user_id').first()] + [pl.sum(f'cluster_{x}') / pl.col(f'cluster_{x}').len() for x in range(len(similarity_matrix))]
            )
            .group_by(
                'user_id'
            )
            .agg(
                [pl.sum(f'cluster_{x}') for x in range(len(similarity_matrix))]
            )
            # Infer primary cluster
            .with_columns(
                pl.struct([pl.col(f'cluster_{x}') for x in range(len(similarity_matrix))]).map_elements(lambda x: self.__infer_clusters(x, model), return_dtype=pl.Int32).alias("predicted_cluster")
            )
            # Select similar clusters
            .with_columns(
                pl.col('predicted_cluster').map_elements(lambda x: similarity_matrix[f'column_{x}'][:3], return_dtype=pl.List(pl.Int32)).alias('predicted_clusters'),
            )
        ).collect().get_column('predicted_clusters').to_list()[0]

    def __get_target_news_ids(self, model_id: str, predicted_clusters: list[int]) -> list[str]:
        news_data = self.repo.get_news_data(model_id)

        return (
            news_data.lazy()
            .filter(pl.col('cluster').is_in(predicted_clusters))
            .sort('issued', descending=True)
            .head(10)
        ).collect().get_column('page').to_list()

    def __build_features_index(self, row, feature_weights):
        viewed_at = row['viewed_at_scaled']
        scroll_percentage = row['scroll_percentage_scaled']
        time_on_page = row['time_on_page_scaled']
        page_visits_count = 0
        viewed_at_weight = feature_weights['timestampHistory_norm'][0]
        scroll_percentage_weight = feature_weights['scrollPercentageHistory_norm'][0]
        time_on_page_weight = feature_weights['timeOnPageHistory_norm'][0]
        page_visits_count_weight = feature_weights['pageVisitsCountHistory_norm'][0]

        index_sum = viewed_at * viewed_at_weight + scroll_percentage * scroll_percentage_weight + time_on_page * time_on_page_weight + page_visits_count * page_visits_count_weight
        return index_sum / (viewed_at_weight + scroll_percentage_weight + time_on_page_weight + page_visits_count_weight)

    def __infer_clusters(self, features, model):
        features = np.array([v for _, v in features.items()])  # Convert to numpy array
        features = torch.from_numpy(features).float()
        features = features.unsqueeze(0)
        outputs = model(features)
        _, predicted = torch.max(outputs, 1)
        return predicted.item()
