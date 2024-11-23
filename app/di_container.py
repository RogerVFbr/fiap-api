from dependency_injector import containers, providers

from services.inference_service import InferenceService
from insfrastructure.aws_s3_client import AwsS3Client
from repositories.inference_repository import InferenceRepository
from repositories.embrapa_repository import EmbrapaRepository
from services.embrapa_service import EmbrapaService


class DiContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["controllers"])

    aws_s3_client = providers.Factory(AwsS3Client)

    embrapa_repository = providers.Factory(EmbrapaRepository)
    inference_repository = providers.Factory(InferenceRepository, client=aws_s3_client)

    inference_service = providers.Factory(InferenceService, repo=inference_repository)
    embrapa_service = providers.Factory(EmbrapaService, empraba_repository=embrapa_repository)
