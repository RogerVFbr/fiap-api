import pandas as pd
from functools import lru_cache
import os


# noinspection PyBroadException
class EmbrapaRepository:

    BASE_PATH = os.path.join(os.getcwd(), 'app', 'embrapa_proxy', 'data')

    PRODUCAO_FILE_PATH = os.path.join(BASE_PATH, 'producao.csv')
    PROCESSAMENTO_FILE_PATH = os.path.join(BASE_PATH, 'processamento.csv')
    COMERCIALIZACAO_FILE_PATH = os.path.join(BASE_PATH, 'comercializacao.csv')

    def __init__(self):
        pd.set_option("display.max_columns", 15)
        pd.set_option("expand.frame_repr", False)
        pd.set_option("display.max_colwidth", None)

    @lru_cache(maxsize=None)
    def get_all_producao(self):
        df = pd.read_csv(self.PRODUCAO_FILE_PATH, sep=";")
        return self.__parse_df_as_dict(df)

    @lru_cache(maxsize=None)
    def get_all_processamento(self):
        df = pd.read_csv(self.PROCESSAMENTO_FILE_PATH, sep="\\s+", usecols=[*range(56)])
        return self.__parse_df_as_dict(df)

    @lru_cache(maxsize=None)
    def get_all_comercializacao(self):
        df = pd.read_csv(self.COMERCIALIZACAO_FILE_PATH, sep=";", header=None)
        columns_names = ["id", "produto_discard", "produto"]
        years = [str(x) for x in range(1970, 2023, 1)]
        columns_names += years
        df.columns = columns_names
        df.drop('produto_discard', axis=1, inplace=True)
        df['produto'] = df['produto'].apply(lambda x: x.strip())
        return self.__parse_df_as_dict(df)

    @lru_cache(maxsize=None)
    def get_all_importacao(self):
        files = [f for f in os.listdir(self.BASE_PATH) if f.startswith('importacao') and f.endswith('.csv')]
        df = pd.concat([pd.read_csv(os.path.join(self.BASE_PATH, f), sep=";") for f in files])
        df.rename(columns={'Id': 'id', 'Categoria': 'categoria', 'País': 'pais'}, inplace=True)

        df_qtd = df.drop(df.filter(regex='\\.1').columns, axis=1)
        data_qtd = self.__parse_df_as_dict(df_qtd)
        data_qtd = [{'historico_qtd' if key == 'historico' else key: value for key, value in d.items()} for d in data_qtd]

        qtd_numeric_cols = [x for x in df_qtd.columns if str(x).isnumeric()]
        df_vlr = df.drop(columns=qtd_numeric_cols)
        df_vlr.columns = df_vlr.columns.str.replace('.1', '')
        data_vlr = self.__parse_df_as_dict(df_vlr)
        data_vlr = [{'historico_vlr' if key == 'historico' else key: value for key, value in d.items()} for d in data_vlr]

        return [{**x[0], **x[1]} for x in zip(data_qtd, data_vlr)]

    @lru_cache(maxsize=None)
    def get_all_exportacao(self):
        files = [f for f in os.listdir(self.BASE_PATH) if f.startswith('exportacao') and f.endswith('.csv')]
        df = pd.concat([pd.read_csv(os.path.join(self.BASE_PATH, f), sep=";") for f in files])
        df.rename(columns={'Id': 'id', 'Categoria': 'categoria', 'País': 'pais'}, inplace=True)

        df_qtd = df.drop(df.filter(regex='\\.1').columns, axis=1)
        data_qtd = self.__parse_df_as_dict(df_qtd)
        data_qtd = [{'historico_qtd' if key == 'historico' else key: value for key, value in d.items()} for d in data_qtd]

        qtd_numeric_cols = [x for x in df_qtd.columns if str(x).isnumeric()]
        df_vlr = df.drop(columns=qtd_numeric_cols)
        df_vlr.columns = df_vlr.columns.str.replace('.1', '')
        data_vlr = self.__parse_df_as_dict(df_vlr)
        data_vlr = [{'historico_vlr' if key == 'historico' else key: value for key, value in d.items()} for d in data_vlr]

        return [{**x[0], **x[1]} for x in zip(data_qtd, data_vlr)]

    def __parse_df_as_dict(self, df: pd.DataFrame) -> dict:
        data_raw = df.to_dict("records")
        data = []

        for entry_raw in data_raw:
            entry = {}

            for key, value in entry_raw.items():
                if key.isnumeric():
                    if "historico" not in entry:
                        entry["historico"] = {}
                    entry["historico"][key] = self.__convert_to_int(value)
                else:
                    entry[key] = value

            data.append(entry)

        return data

    @staticmethod
    def __convert_to_int(value):
        try:
            return int(value)
        except:
            return None

