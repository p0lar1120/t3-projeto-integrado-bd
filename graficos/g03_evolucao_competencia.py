"""Figura 03: quantidade aprovada por competência de atendimento."""
import matplotlib.pyplot as plt

from graficos.comum import AZUL, carregar_dados, salvar


def gerar(dados):
    evolucao = dados.df.groupby("AnoMes")["pa_qtdapr"].sum().rename("QtdAprovada").reset_index()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(evolucao["AnoMes"], evolucao["QtdAprovada"], color=AZUL)
    for x, v in zip(evolucao["AnoMes"], evolucao["QtdAprovada"]):
        ax.text(x, v, f"{v:,.0f}", ha="center", va="bottom", fontsize=9)
    ax.set_title("Quantidade aprovada por competência de atendimento (arquivo PARS 07/2026)")
    ax.set_xlabel("Competência (AAAAMM)"); ax.set_ylabel("Quantidade aprovada")
    salvar("03_evolucao_competencia")


if __name__ == "__main__":
    gerar(carregar_dados())
