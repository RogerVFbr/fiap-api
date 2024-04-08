from dependency_injector import containers, providers

from repositories.embrapa_repository import EmbrapaRepository
from services.embrapa_service import EmbrapaService


class DiContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["controllers"])

    embrapa_repository = providers.Factory(EmbrapaRepository)

    embrapa_service = providers.Factory(EmbrapaService, empraba_repository=embrapa_repository)
