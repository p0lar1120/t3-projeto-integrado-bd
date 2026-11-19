"""Figura 08: valor produzido x aprovado por grupo e gasto médio por procedimento."""
import matplotlib.pyplot as plt

from graficos.comum import AZUL, LARANJA, carregar_dados, salvar


def gerar(dados):
    df = dados.df
    fin_grupo = df.groupby("Grupo").agg(ValorProduzido=("pa_valpro", "sum"), ValorAprovado=("pa_valapr", "sum"))

    # Gasto médio por unidade de procedimento aprovado, por competência
    gasto = df.groupby("AnoMes")[["pa_valapr", "pa_qtdapr"]].sum()
    gasto = gasto["pa_valapr"] / gasto["pa_qtdapr"]
    sem_med = df[~df["Grupo"].str.contains("edicamento")].groupby("AnoMes")[["pa_valapr", "pa_qtdapr"]].sum()
    gasto_sm = sem_med["pa_valapr"] / sem_med["pa_qtdapr"]

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
    fg = fin_grupo.sort_values("ValorProduzido")[["ValorProduzido", "ValorAprovado"]]
    fg.index = [i[:35] for i in fg.index]
    fg.plot(kind="barh", ax=axes[0], color=[LARANJA, AZUL])
    axes[0].set_title("Valor produzido x aprovado por grupo (R$)"); axes[0].set_ylabel(""); axes[0].legend(["Produzido", "Aprovado"])
    gasto.plot(ax=axes[1], marker="o", color=AZUL, label="Total")
    gasto_sm.plot(ax=axes[1], marker="s", color=LARANJA, label="Sem medicamentos")
    axes[1].set_title("Gasto médio aprovado por procedimento (R$)"); axes[1].set_xlabel("Competência")
    axes[1].set_ylabel("R$ / procedimento"); axes[1].legend()
    axes[1].set_xticks(range(len(gasto))); axes[1].set_xticklabels(gasto.index)
    salvar("08_financeiro")


if __name__ == "__main__":
    gerar(carregar_dados())
