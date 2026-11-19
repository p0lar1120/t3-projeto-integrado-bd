"""Figura 09: oncologia, saúde mental e atenção básica/crônicos."""
import matplotlib.pyplot as plt
import pandas as pd

from graficos.comum import AZUL, LARANJA, carregar_dados, salvar


def tipo_onco(descricao):
    d = descricao.upper()
    if "QUIMIOTERAPIA" in d: return "Quimioterapia"
    if "RADIOTERAPIA" in d: return "Radioterapia"
    if "HORMONIOTERAPIA" in d: return "Hormonioterapia"
    return "Outros (oncologia)"


def gerar(dados):
    df = dados.df

    # Oncologia (grupo 0304): produzido x aprovado
    onco = df[df["pa_proc_id"].str.startswith("0304")].copy()
    onco["Tipo"] = onco["Procedimento"].map(tipo_onco)
    onco_t = onco.groupby("Tipo").agg(QtdProduzida=("pa_qtdpro", "sum"), QtdAprovada=("pa_qtdapr", "sum"))

    # Saúde mental: critérios que se sobrepõem
    sm = df.copy()
    sm["CAPS"] = sm["pa_proc_id"].str.startswith("030108")
    sm["Psicólogo (CBO 2515)"] = sm["pa_cbocod"].str.startswith("2515")
    sm["Psiquiatra (CBO 225133)"] = sm["pa_cbocod"] == "225133"
    sm["CID F (transtornos mentais)"] = sm["CID"].str.startswith("F")
    flags = ["CAPS", "Psicólogo (CBO 2515)", "Psiquiatra (CBO 225133)", "CID F (transtornos mentais)"]
    saude_mental = {f: sm.loc[sm[f], "pa_qtdapr"].sum() for f in flags}

    # Atenção básica/crônicos
    cron = df[df["CategoriaCID"].isin(["Hipertensão (I10-I15)", "Diabetes (E10-E14)",
                                       "Asma/DPOC (J40-J47)", "Doença renal (N17-N19)"])]

    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    onco_t[["QtdProduzida", "QtdAprovada"]].plot(kind="bar", ax=axes[0], color=[LARANJA, AZUL], rot=20)
    axes[0].set_title("Oncologia: produzido x aprovado (qtd)"); axes[0].set_xlabel(""); axes[0].legend(["Produzida", "Aprovada"])

    s = pd.Series(saude_mental).sort_values()
    s.plot(kind="barh", ax=axes[1], color=AZUL)
    for i, v in enumerate(s): axes[1].text(v, i, f" {v:,.0f}", va="center", fontsize=8)
    axes[1].set_title("Saúde mental: qtd. aprovada por critério\n(critérios se sobrepõem)"); axes[1].set_xlabel("Quantidade aprovada")

    c = cron.groupby("CategoriaCID")["pa_qtdapr"].sum().sort_values()
    c.plot(kind="barh", ax=axes[2], color=AZUL)
    axes[2].set_title("Atenção básica/crônicos: qtd. aprovada por CID"); axes[2].set_ylabel(""); axes[2].set_xlabel("Quantidade aprovada")
    salvar("09_areas_criticas")


if __name__ == "__main__":
    gerar(carregar_dados())
