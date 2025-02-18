from dependency_injector.wiring import inject, Provide
from flask_smorest import Blueprint

from app.crosscutting.di_container import DiContainer
from app.news_recommendation.news_recommendation_service import NewsRecommendationService
from app.news_recommendation.schemas.rews_recommendation_request_schema import NewsRecommendationRequestBodySchema
from app.news_recommendation.schemas.rews_recommendation_request_schema import NewsRecommendationRequestQuerySchema
from app.news_recommendation.schemas.rews_recommendation_response_schema import NewsRecommendationResponseSchema

news_recommendation_controller = Blueprint("NewsRecommendationController", __name__, description="News Recommendation API")

@news_recommendation_controller.post("/news-recommendation/infer")
@news_recommendation_controller.arguments(NewsRecommendationRequestBodySchema)
@news_recommendation_controller.arguments(NewsRecommendationRequestQuerySchema, location="query")
@news_recommendation_controller.response(200, NewsRecommendationResponseSchema)
@inject
def post_infer(body, query, service: NewsRecommendationService = Provide[DiContainer.news_recommendation_service]):
    return NewsRecommendationResponseSchema().load({
        "model_name": query.get("name"),
        "model_id": query.get("id"),
        "output": service.infer(query.get("name"), query.get("id"), body['user_id'], body['views'])
    })