"""Figura 05: quantidade aprovada por faixa etária e sexo + 10 CIDs mais frequentes."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from graficos.comum import AZUL, FAIXAS, carregar_dados, salvar


def gerar(dados):
    df = dados.df
    ordem = FAIXAS + ["Não informado"]
    perfil = pd.crosstab(df["FaixaEtaria"], df["Sexo"], values=df["pa_qtdapr"], aggfunc="sum").reindex(ordem).fillna(0)
    cid = (df[df["CID"] != "Não informado"].groupby(["CID", "Diagnostico"])["pa_qtdapr"].size()
           .sort_values(ascending=False).rename("Registros"))

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5), gridspec_kw={"width_ratios": [1, 1.2]})
    sns.heatmap(perfil.drop(index="Não informado"), annot=True, fmt=",.0f", cmap="Blues", ax=axes[0], cbar=False)
    axes[0].set_title("Quantidade aprovada por faixa etária e sexo"); axes[0].set_xlabel(""); axes[0].set_ylabel("Faixa etária")
    c = cid.head(10).copy()
    c.index = [f"{a} - {b[:38]}" for a, b in c.index]
    c.sort_values().plot(kind="barh", ax=axes[1], color=AZUL)
    axes[1].set_title("10 diagnósticos (CID) mais frequentes (registros)"); axes[1].set_ylabel(""); axes[1].set_xlabel("Registros")
    salvar("05_perfil_demografico_cid")


if __name__ == "__main__":
    gerar(carregar_dados())
