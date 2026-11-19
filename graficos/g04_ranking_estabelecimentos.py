"""Figura 04: ranking de estabelecimentos (sem medicamentos) e apresentado x aprovado."""
import matplotlib.pyplot as plt

from graficos.comum import AZUL, LARANJA, carregar_dados, salvar


def gerar(dados):
    df = dados.df
    estab = df.groupby("Estabelecimento").agg(QtdApresentada=("pa_qtdpro", "sum"), QtdAprovada=("pa_qtdapr", "sum"))
    # Sem medicamentos: a dispensação da Coordenadoria Regional de Saúde distorce o ranking por quantidade
    sem_med = (df[~df["Grupo"].str.contains("edicamento")].groupby("Estabelecimento")["pa_qtdapr"].sum()
               .sort_values(ascending=False))

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))
    t = sem_med.head(10).sort_values()
    t.plot(kind="barh", ax=axes[0], color=AZUL)
    for i, v in enumerate(t): axes[0].text(v, i, f" {v:,.0f}", va="center", fontsize=8)
    axes[0].set_title("Ranking de produção aprovada (sem medicamentos)"); axes[0].set_ylabel(""); axes[0].set_xlabel("Quantidade aprovada")
    cmp = estab.nlargest(8, "QtdApresentada")[["QtdApresentada", "QtdAprovada"]].iloc[::-1]
    cmp.plot(kind="barh", ax=axes[1], color=[LARANJA, AZUL])
    axes[1].set_title("Apresentado x aprovado (8 maiores, incl. medicamentos)"); axes[1].set_ylabel(""); axes[1].set_xlabel("Quantidade")
    axes[1].legend(["Apresentada", "Aprovada"])
    salvar("04_ranking_estabelecimentos")


if __name__ == "__main__":
    gerar(carregar_dados())
