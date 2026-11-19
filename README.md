# T3 - Análise de dados do SIASUS para apoio à gestão municipal de saúde (Ijuí/RS)

Solução que armazena (MySQL/MariaDB), processa (Pandas) e visualiza (Matplotlib/Seaborn) a produção ambulatorial do SUS
para apoiar a Secretaria Municipal de Saúde de Ijuí.

## Fontes e período analisado
| Fonte | Descrição |
|---|---|
| DATASUS / SIASUS | `PARS2607` - Produção Ambulatorial (PA) do RS, **competência de movimentação 07/2026** (competências de atendimento 04 a 07/2026; 4.532.294 registros, 68.827 de Ijuí) |
| DATASUS / TABWIN | Tabelas auxiliares: `CADGERRS` (estabelecimentos), `CBO`, `S_CID` (CID-10), `TB_SIGTAW` (procedimentos), `TB_GRUPO`, `TB_SUBGR` etc. |
| DATASUS | Base territorial (`tb_municip` e relacionamentos), jun/2026 |

O recorte é o município de Ijuí (`PA_UFMUN = '431020'`). Os dados brutos (`dados/`) não são versionados.

## Estrutura
```
conexao.py                 conexão MySQL (usa ~/.my.cnf se existir; senão pede usuário e senha)
importar_dbf.py            carrega os .dbf auxiliares no schema `sia`
consulta.py                função auxiliar de consulta -> DataFrame
sql/01_criar_banco.sql     banco `sia` e tabela pars2607
sql/02_carga_pars.sql      LOAD DATA INFILE do PARS2607.csv
sql/03_dimtempo.sql        tabela de granularidade temporal (mês, bimestre, trimestre, semestre)
sql/04_indices.sql         índices para os JOINs
sql/05_view_pa_ijui.sql    VIEW sia.pa_ijui (Ijuí + tabelas descritivas)
sql/06_validacao_consultas.sql   validação e consultas de demonstração
gerar_graficos.py          gera as 9 figuras fora do notebook (aceita números: gerar_graficos.py 02 07)
graficos/                  um módulo por figura (g01_... a g09_...) + comum.py (carga, limpeza, estilo)
analise_siasus.ipynb       Aulas 2 e 3: exploração, limpeza, análises, gráficos e interpretação
figuras/                   gráficos gerados pelo notebook
```
Modelo (conforme enunciado): PARS ligada a cadgerrs (`pa_coduni`), município (`pa_ufmun`/`pa_munpcn`),
procedimento (`pa_proc_id`), CBO (`pa_cbocod`) e CID10 (`pa_cidpri`); município ligado à região de saúde e microrregião.

## Como reproduzir
1. **Obter e converter:** baixar do DATASUS o `PARS2607.dbc` e as tabelas auxiliares; converter `.dbc` para `.dbf` e examinar os
   campos no TABWIN; exportar o PARS para CSV (`dados/PARS2607.csv`).
2. **Dependências:** `python -m venv .venv && .venv/bin/pip install pandas mysql-connector-python dbfread matplotlib seaborn jupyter`
3. **Credenciais:** criar `~/.my.cnf` (`[client]`, `user=`, `password=`) ou informar usuário/senha quando solicitado.
4. **Banco (nesta ordem):**
   ```
   mysql --local-infile=1 < sql/01_criar_banco.sql      # atenção: recria a tabela pars2607
   mysql --local-infile=1 < sql/02_carga_pars.sql       # executar na raiz do projeto
   .venv/bin/python importar_dbf.py                     # tabelas auxiliares
   mysql < sql/03_dimtempo.sql
   mysql < sql/04_indices.sql
   mysql < sql/05_view_pa_ijui.sql
   mysql -t < sql/06_validacao_consultas.sql            # validação
   ```
   Validação esperada: `pars2607` = 4.532.294 linhas (o CSV tem 4.532.295 com o cabeçalho); `pa_ijui` = 68.827 linhas (iguais às de `pars2607` com `PA_UFMUN='431020'`).
5. **Análises e gráficos:** `.venv/bin/jupyter nbconvert --to notebook --execute --inplace analise_siasus.ipynb`
   (ou abrir o notebook no Jupyter). Os gráficos são gravados em `figuras/`.
   Os mesmos gráficos também podem ser gerados sem o notebook: `.venv/bin/python gerar_graficos.py`.

## Decisões e observações
- A VIEW liga a dimensão tempo à **competência de atendimento** (`PA_CMP`): o mês de movimentação (`PA_MVM`) é único no arquivo.
- A tabela `cid` tem códigos repetidos em minúsculas (ex.: `j450`, "CID não identificado"); a VIEW usa só os códigos em maiúsculas para não duplicar linhas.
- **Limpeza:** sexo diferente de M/F, idade 999 e CID `0000` viram "Não informado" (sem excluir linhas); duplicatas exatas são removidas
  (a chave `REMOVER_DUPLICADOS` do notebook permite comparar; a remoção reduz 6,7% da quantidade aprovada).
- Existe apenas um mês de movimentação, então não há tendência temporal; o SIASUS de Ijuí não traz UBS (atenção básica está no e-SUS APS).
- Descrições de alguns procedimentos têm caracteres corrompidos na origem (codificação do DBF).

## Principais resultados (resumo)
Aprovados ~340 mil procedimentos e R$ 5,7 mi (98,5% do apresentado); 59% da quantidade é medicamento (17ª CRS);
~63% dos atendimentos com município válido são de moradores de outros municípios (Panambi, Joia, Crissiumal, Catuípe...);
Hospital de Clínicas concentra a oncologia; Bom Pastor aprova só 59% da quantidade apresentada. Detalhes e gráficos em `analise_siasus.ipynb`.
