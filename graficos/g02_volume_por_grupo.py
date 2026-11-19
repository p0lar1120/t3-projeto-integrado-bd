"""Figura 02: quantidade aprovada por grupo e 10 maiores subgrupos (sem medicamentos)."""
import matplotlib.pyplot as plt

from graficos.comum import AZUL, carregar_dados, salvar


def gerar(dados):
    df = dados.df
    por_grupo = df.groupby("Grupo")["pa_qtdapr"].sum().sort_values(ascending=False)
    por_subgrupo = df.groupby("Subgrupo")["pa_qtdapr"].sum().sort_values(ascending=False)

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
    g = por_grupo.sort_values()
    g.plot(kind="barh", ax=axes[0], color=AZUL)
    for i, v in enumerate(g): axes[0].text(v, i, f" {v:,.0f}", va="center", fontsize=8)
    axes[0].set_title("Quantidade aprovada por grupo de procedimentos"); axes[0].set_xlabel(""); axes[0].set_ylabel("")
    sg = por_subgrupo.drop(index=[s for s in por_subgrupo.index if "edicamento" in s], errors="ignore").head(10).sort_values()
    sg.plot(kind="barh", ax=axes[1], color=AZUL)
    axes[1].set_title("10 maiores subgrupos (sem medicamentos)"); axes[1].set_xlabel("Quantidade aprovada"); axes[1].set_ylabel("")
    salvar("02_volume_por_grupo")


if __name__ == "__main__":
    gerar(carregar_dados())
