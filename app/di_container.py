from dependency_injector import containers, providers

from app.insfrastructure.aws_s3_client import AwsS3Client
from app.repositories.embrapa_repository import EmbrapaRepository
from app.repositories.inference_repository import InferenceRepository
from app.services.embrapa_service import EmbrapaService
from app.services.inference_service import InferenceService


class DiContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["app.controllers"])

    aws_s3_client = providers.Factory(AwsS3Client)

    embrapa_repository = providers.Factory(EmbrapaRepository)
    inference_repository = providers.Factory(InferenceRepository, client=aws_s3_client)

    inference_service = providers.Factory(InferenceService, repo=inference_repository)
    embrapa_service = providers.Factory(EmbrapaService, empraba_repository=embrapa_repository)
