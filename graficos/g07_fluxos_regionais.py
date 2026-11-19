"""Figura 07: municípios de origem dos pacientes e residência (Ijuí x outros)."""
import matplotlib.pyplot as plt
import numpy as np

from graficos.comum import AZUL, CINZA, LARANJA, carregar_dados, salvar

COD_IJUI = "431020"


def gerar(dados):
    df = dados.df.copy()
    df["Residente"] = np.where(df["pa_munpcn"] == COD_IJUI, "Ijuí", "Outros municípios")
    # 999999 = município inválido/ignorado (registros consolidados, sem identificação do paciente)
    df.loc[df["pa_munpcn"].isin(["", "000000", "999999"]) | df["pa_munpcn"].isna(), "Residente"] = "Não informado"

    res = df.groupby("Residente")["pa_qtdapr"].size().rename("Registros")
    origem = (df[df["Residente"] != "Não informado"].groupby(["pa_munpcn", "MunicipioPaciente"])["pa_qtdapr"].size()
              .sort_values(ascending=False).rename("Registros").reset_index())

    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5), gridspec_kw={"width_ratios": [1.5, 1]})
    o = origem[origem["pa_munpcn"] != COD_IJUI].head(10).set_index("MunicipioPaciente")["Registros"].sort_values()
    o.plot(kind="barh", ax=axes[0], color=AZUL)
    for i, v in enumerate(o): axes[0].text(v, i, f" {v:,.0f}", va="center", fontsize=8)
    axes[0].set_title("10 principais municípios de origem (exceto Ijuí)"); axes[0].set_ylabel(""); axes[0].set_xlabel("Registros")
    axes[1].pie(res, labels=res.index, autopct="%1.1f%%", startangle=90, colors=[AZUL, LARANJA, CINZA][:len(res)],
                wedgeprops={"width": 0.45})
    axes[1].set_title("Residência do paciente (registros)")
    salvar("07_fluxos_regionais")


if __name__ == "__main__":
    gerar(carregar_dados())
