"""Gera todas as figuras do projeto em figuras/*.png, fora do notebook.

Uso (na raiz do projeto, com o banco `sia` carregado):
    .venv/bin/python gerar_graficos.py            # todas as figuras
    .venv/bin/python gerar_graficos.py 02 07      # só as figuras indicadas
Cada figura também pode ser gerada isoladamente: python -m graficos.g02_volume_por_grupo
"""
import sys

from graficos.comum import carregar_dados
from graficos import (g01_ausentes, g02_volume_por_grupo, g03_evolucao_competencia,
                      g04_ranking_estabelecimentos, g05_perfil_demografico_cid, g06_categorias_cid,
                      g07_fluxos_regionais, g08_financeiro, g09_areas_criticas)

FIGURAS = {
    "01": g01_ausentes, "02": g02_volume_por_grupo, "03": g03_evolucao_competencia,
    "04": g04_ranking_estabelecimentos, "05": g05_perfil_demografico_cid, "06": g06_categorias_cid,
    "07": g07_fluxos_regionais, "08": g08_financeiro, "09": g09_areas_criticas,
}


if __name__ == "__main__":
    escolhidas = sys.argv[1:] or list(FIGURAS)
    dados = carregar_dados()
    for numero in escolhidas:
        FIGURAS[numero].gerar(dados)
