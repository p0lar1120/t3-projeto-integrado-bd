from pathlib import Path
from dbfread import DBF
from conexao import usar_conexao

SCHEMA = "sia"
PASTA = Path(__file__).parent / "dados"
# Já importados na primeira carga (cópias idênticas em TAB_SIA/DBF são ignoradas)
JA_IMPORTADOS = {"cadgerrs", "cbo", "s_cid", "tb_sigtaw"}
PASTAS = [PASTA / "06-base_territorial_jun26", PASTA / "TAB_SIA" / "DBF"]
LOTE = 5000


def tipo_sql(campo):
    if campo.type == "C":
        return f"VARCHAR({campo.length})"
    if campo.type == "D":
        return "DATE"
    if campo.type == "N":
        if campo.decimal_count:
            return f"DECIMAL({campo.length},{campo.decimal_count})"
        return "BIGINT"
    if campo.type == "L":
        return "BOOLEAN"
    raise ValueError(f"Tipo DBF não suportado: {campo.name} ({campo.type})")


def importar(connection, caminho):
    tabela = DBF(str(caminho), encoding="latin-1", load=False)
    nome = caminho.stem.lower()
    colunas = [f.name.lower() for f in tabela.fields]
    ddl = ", ".join(f"`{f.name.lower()}` {tipo_sql(f)}" for f in tabela.fields)
    insert = (f"INSERT INTO `{SCHEMA}`.`{nome}` ({', '.join(f'`{c}`' for c in colunas)}) "
              f"VALUES ({', '.join(['%s'] * len(colunas))})")

    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS `{SCHEMA}`.`{nome}`")
        cursor.execute(f"CREATE TABLE `{SCHEMA}`.`{nome}` ({ddl}) "
                       "DEFAULT CHARSET=utf8mb4")
        lote, total = [], 0
        for registro in tabela:
            lote.append(tuple(registro.values()))
            if len(lote) == LOTE:
                cursor.executemany(insert, lote)
                total += len(lote)
                lote = []
        if lote:
            cursor.executemany(insert, lote)
            total += len(lote)
    connection.commit()
    print(f"{nome}: {total} linhas importadas")


def acao(connection):
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{SCHEMA}`")
    arquivos = sorted(f for pasta in PASTAS for f in pasta.iterdir()
                      if f.suffix.lower() == ".dbf"
                      and f.stem.lower() not in JA_IMPORTADOS)
    for arquivo in arquivos:
        importar(connection, arquivo)


if __name__ == "__main__":
    usar_conexao(acao)
