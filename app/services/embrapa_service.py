from typing import List

from repositories.embrapa_repository import EmbrapaRepository


class EmbrapaService:

    def __init__(self, empraba_repository: EmbrapaRepository):
        self._empraba_repository = empraba_repository

    def get_all_producao(self) -> List:
        return self._empraba_repository.get_all_producao()

    def get_all_processamento(self) -> List:
        return self._empraba_repository.get_all_processamento()

    def get_all_comercializacao(self) -> List:
        return self._empraba_repository.get_all_comercializacao()

    def get_all_importacao(self) -> List:
        return self._empraba_repository.get_all_importacao()

    def get_all_exportacao(self) -> List:
        return self._empraba_repository.get_all_exportacao()
