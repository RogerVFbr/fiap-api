from dependency_injector import containers, providers

from app.crosscutting.aws_s3_client import AwsS3Client
from app.embrapa_proxy.embrapa_repository import EmbrapaRepository
from app.news_recommendation.news_recommendation_repository import NewsRecommendationRepository
from app.news_recommendation.news_recommendation_service import NewsRecommendationService
from app.stock_price.stock_price_repository import StockPriceRepository
from app.embrapa_proxy.embrapa_service import EmbrapaService
from app.stock_price.stock_price_service import StockPriceService


class DiContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=[
        "app.embrapa_proxy",
        "app.stock_price",
        "app.news_recommendation",
        "app.warmup"
    ])

    aws_s3_client = providers.Factory(AwsS3Client)

    embrapa_repository = providers.Factory(EmbrapaRepository)
    stock_price_repository = providers.Factory(StockPriceRepository, client=aws_s3_client)
    news_recommendation_repository = providers.Factory(NewsRecommendationRepository, client=aws_s3_client)

    stock_price_service = providers.Factory(StockPriceService, repo=stock_price_repository)
    news_recommendation_service = providers.Factory(NewsRecommendationService, repo=news_recommendation_repository)
    embrapa_service = providers.Factory(EmbrapaService, empraba_repository=embrapa_repository)
