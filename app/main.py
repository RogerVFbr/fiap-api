import json

from repositories.embrapa_repository import EmbrapaRepository


def test():
    repo = EmbrapaRepository()
    # data = repo.get_all_producao()
    # data = repo.get_all_processamento()
    # data = repo.get_all_comercializacao()
    # data = repo.get_all_importacao()
    data = repo.get_all_exportacao()
    print(json.dumps(data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    test()