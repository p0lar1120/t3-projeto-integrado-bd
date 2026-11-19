"""Figura 06: registros por grande grupo de diagnóstico (CID informado)."""
import matplotlib.pyplot as plt

from graficos.comum import AZUL, carregar_dados, salvar


def gerar(dados):
    df = dados.df
    cat = (df[df["CategoriaCID"] != "Sem CID"].groupby("CategoriaCID")["pa_qtdapr"].size()
           .sort_values(ascending=False).rename("Registros"))

    fig, ax = plt.subplots(figsize=(8, 4))
    cat.sort_values().plot(kind="barh", ax=ax, color=AZUL)
    ax.set_title("Registros por grande grupo de diagnóstico (CID informado)"); ax.set_ylabel(""); ax.set_xlabel("Registros")
    salvar("06_categorias_cid")


if __name__ == "__main__":
    gerar(carregar_dados())
