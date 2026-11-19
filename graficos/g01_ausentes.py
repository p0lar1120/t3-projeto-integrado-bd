"""Figura 01: valores ausentes por atributo."""
import matplotlib.pyplot as plt

from graficos.comum import AZUL, carregar_dados, salvar


def gerar(dados):
    ausentes = dados.bruto.isna().sum().sort_values(ascending=False)
    ausentes = ausentes[ausentes > 0].sort_values()
    if len(ausentes):
        ausentes.plot(kind="barh", figsize=(9, 4), color=AZUL)
        plt.title("Valores ausentes por atributo (após junção com tabelas descritivas)")
        plt.xlabel("Quantidade de registros")
        salvar("01_ausentes")


if __name__ == "__main__":
    gerar(carregar_dados())
