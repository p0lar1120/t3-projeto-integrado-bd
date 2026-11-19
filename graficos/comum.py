"""Carga, preparação dos dados e utilitários compartilhados pelos gráficos.

Reproduz as etapas de carga (seção 1) e limpeza (seção 3) do notebook analise_siasus.ipynb.
"""
import os
from types import SimpleNamespace

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from consulta import consultar

AZUL, LARANJA, CINZA = "#2a6f97", "#e07a1f", "#8a8f98"   # apresentado/aprovado e neutro
PASTA_FIGURAS = "figuras"
NUM = ["pa_qtdpro", "pa_qtdapr", "pa_valpro", "pa_valapr"]
FAIXAS = ["0-4", "5-11", "12-17", "18-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]


def configurar_estilo():
    sns.set_theme(style="whitegrid", font_scale=0.95)
    os.makedirs(PASTA_FIGURAS, exist_ok=True)


def salvar(nome):
    """Grava a figura corrente em figuras/<nome>.png e a fecha."""
    plt.tight_layout()
    plt.savefig(f"{PASTA_FIGURAS}/{nome}.png", dpi=130, bbox_inches="tight")
    plt.close()
    print(f"Figura gerada: {PASTA_FIGURAS}/{nome}.png")


def categoria(cid):
    """Agrupa o CID em grandes categorias de diagnóstico."""
    if cid == "Não informado": return "Sem CID"
    if "I10" <= cid[:3] <= "I15": return "Hipertensão (I10-I15)"
    if "E10" <= cid[:3] <= "E14": return "Diabetes (E10-E14)"
    if cid[0] == "C" or ("D00" <= cid[:3] <= "D48"): return "Câncer/neoplasias (C00-D48)"
    if cid[0] == "F": return "Transtornos mentais (F)"
    if "J40" <= cid[:3] <= "J47": return "Asma/DPOC (J40-J47)"
    if cid[0] == "N" and cid[:3] in ("N17", "N18", "N19"): return "Doença renal (N17-N19)"
    return "Outros"


def carregar_dados(remover_duplicados=True):
    """Lê a VIEW sia.pa_ijui, limpa e devolve um objeto com `bruto`, `df` e `tempo`.

    - bruto: dados como vieram do banco (com os campos numéricos convertidos);
    - df: dados tratados (valores inválidos -> "Não informado", duplicatas removidas);
    - tempo: dimensão tempo (DIMTEMPO).
    """
    configurar_estilo()

    bruto = consultar("SELECT * FROM sia.pa_ijui")
    grupos = consultar("SELECT co_grupo, no_grupo AS grupo FROM sia.tb_grupo")
    grupos["grupo"] = grupos["grupo"].str.strip()   # o grupo 09 vem com \r\n no DBF
    subgrupos = consultar("SELECT co_sub_gru, no_sub_gru AS subgrupo FROM sia.tb_subgr")
    subgrupos["subgrupo"] = subgrupos["subgrupo"].str.strip()
    tempo = consultar("SELECT Id, anomes, MAExt, anobi, anotri FROM sia.DIMTEMPO ORDER BY Id")

    for c in NUM:
        bruto[c] = pd.to_numeric(bruto[c])

    df = bruto.copy()
    df["Sexo"] = df["pa_sexo"].map({"M": "Masculino", "F": "Feminino"}).fillna("Não informado")
    df["Idade"] = pd.to_numeric(df["pa_idade"], errors="coerce").where(lambda s: s.between(0, 120))
    df["FaixaEtaria"] = pd.cut(df["Idade"], bins=[-1, 4, 11, 17, 29, 39, 49, 59, 69, 79, 120],
                               labels=FAIXAS).astype(object).fillna("Não informado")
    df["CID"] = np.where(df["pa_cidpri"].isin(["0000", ""]), "Não informado", df["pa_cidpri"])
    df["Diagnostico"] = np.where(df["CID"] == "Não informado", "Não informado",
                                 df["Diagnostico"].fillna("CID não cadastrado"))
    for col in ["Estabelecimento", "Procedimento", "Ocupacao", "MunicipioPaciente", "MunicipioEstabelecimento"]:
        df[col] = df[col].fillna("Não informado")
    df["Grupo"] = df["pa_proc_id"].str[:2].map(grupos.set_index("co_grupo")["grupo"]).fillna("Não informado")
    df["Subgrupo"] = df["pa_proc_id"].str[:4].map(subgrupos.set_index("co_sub_gru")["subgrupo"]).fillna("Não informado")

    if remover_duplicados:
        df = df.drop_duplicates().reset_index(drop=True)

    df["CategoriaCID"] = df["CID"].map(categoria)
    return SimpleNamespace(bruto=bruto, df=df, tempo=tempo)
