import pandas as pd
from conexao import usar_conexao


def consultar(sql, params=None):
    """Executa um SELECT e devolve o resultado como DataFrame."""
    def acao(connection):
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            colunas = [c[0] for c in cursor.description]
            return pd.DataFrame(cursor.fetchall(), columns=colunas)
    return usar_conexao(acao)


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)  # mostra todas as colunas
    pd.set_option("display.width", 200)

    df = consultar("SELECT * FROM sia.pars2607 LIMIT 100")
    if df is not None:
        print(df.shape)
        print(df.head(20))
        print(df.dtypes)
