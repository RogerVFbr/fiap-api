import pandas as pd
from functools import lru_cache


# noinspection PyBroadException
class EmbrapaRepository:

    def __init__(self):
        pd.set_option("display.max_columns", 15)
        pd.set_option("expand.frame_repr", False)
        pd.set_option("display.max_colwidth", None)

    @lru_cache(maxsize=None)
    def get_all_producao(self):
        df = pd.read_csv('data/producao.csv', sep=";")
        return self.__parse_df_as_dict(df)

    @lru_cache(maxsize=None)
    def get_all_processamento(self):
        df = pd.read_csv('data/processamento.csv', sep="\\s+", usecols=[*range(56)])
        return self.__parse_df_as_dict(df)

    @lru_cache(maxsize=None)
    def get_all_comercializacao(self):
        df = pd.read_csv('data/comercializacao.csv', sep=";", header=None)
        columns_names = ["id", "produto_discard", "produto"]
        years = [str(x) for x in range(1970, 2023, 1)]
        columns_names += years
        df.columns = columns_names
        df.drop('produto_discard', axis=1, inplace=True)
        df['produto'] = df['produto'].apply(lambda x: x.strip())
        return self.__parse_df_as_dict(df)

    @lru_cache(maxsize=None)
    def get_all_importacao(self):
        dfs = []

        df_mesa = pd.read_csv('data/importacao_vinhos_de_mesa.csv', sep=";")
        df_mesa['Categoria'] = 'Vinhos de Mesa'
        dfs.append(df_mesa)

        df_espumantes = pd.read_csv('data/importacao_espumantes.csv', sep=";")
        df_espumantes['Categoria'] = 'Espumantes'
        dfs.append(df_espumantes)

        df_frescas = pd.read_csv('data/importacao_frescas.csv', sep=";")
        df_frescas['Categoria'] = 'Uvas Frescas'
        dfs.append(df_frescas)

        df_passas = pd.read_csv('data/importacao_passas.csv', sep=";")
        df_passas['Categoria'] = 'Uvas Passas'
        dfs.append(df_passas)

        df_suco = pd.read_csv('data/importacao_suco.csv', sep=";")
        df_suco['Categoria'] = 'Suco de Uva'
        df_suco.rename(columns={'2021.2': '2022', '2021.3': '2022.1'}, inplace=True)
        dfs.append(df_suco)

        df = pd.concat(dfs, ignore_index=True)
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
        dfs = []

        df_mesa = pd.read_csv('data/exportacao_vinhos_de_mesa.csv', sep=";")
        df_mesa['Categoria'] = 'Vinhos de Mesa'
        dfs.append(df_mesa)

        df_espumantes = pd.read_csv('data/exportacao_espumantes.csv', sep=";")
        df_espumantes['Categoria'] = 'Espumantes'
        dfs.append(df_espumantes)

        df_frescas = pd.read_csv('data/exportacao_uva.csv', sep=";")
        df_frescas['Categoria'] = 'Uvas Frescas'
        dfs.append(df_frescas)

        df_suco = pd.read_csv('data/exportacao_suco.csv', sep=";")
        df_suco['Categoria'] = 'Suco de Uva'
        dfs.append(df_suco)

        df = pd.concat(dfs, ignore_index=True)
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
        # print(df.columns)
        # print(len(df.columns))
        # print(df.head())

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

