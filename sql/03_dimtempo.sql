-- Tabela de granularidade temporal (um registro por mês, 2010-01 a 2026-11).
USE sia;
DROP TABLE IF EXISTS DIMTEMPO;
CREATE TABLE DIMTEMPO (
  Id        SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  di        DATE NOT NULL,
  df        DATE AS (LAST_DAY(di)) STORED,
  mes       TINYINT AS (MONTH(di)) STORED,
  mesext    VARCHAR(20) AS (ELT(MONTH(di),'janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro')) STORED,
  ano       SMALLINT AS (YEAR(di)) STORED,
  anomes    CHAR(6) AS (CONCAT(YEAR(di), LPAD(MONTH(di),2,'0'))) STORED,
  MAExt     VARCHAR(10) AS (CONCAT(ELT(MONTH(di),'jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'),'-',YEAR(di))) STORED,
  bimestre  TINYINT AS ((MONTH(di)-1) DIV 2 + 1) STORED,
  bi_inicio DATE AS (MAKEDATE(YEAR(di),1) + INTERVAL (MONTH(di)-1) DIV 2 * 2 MONTH) STORED,
  bi_fim    DATE AS (LAST_DAY(bi_inicio + INTERVAL 1 MONTH)) STORED,
  biex_t    VARCHAR(20) AS (CONCAT((MONTH(di)-1) DIV 2 + 1,'º bimestre')) STORED,
  anobi     CHAR(7) AS (CONCAT(YEAR(di),'B',(MONTH(di)-1) DIV 2 + 1)) STORED,
  trimestre TINYINT AS (QUARTER(di)) STORED,
  tri_inicio DATE AS (MAKEDATE(YEAR(di),1) + INTERVAL (QUARTER(di)-1)*3 MONTH) STORED,
  tri_fim   DATE AS (LAST_DAY(tri_inicio + INTERVAL 2 MONTH)) STORED,
  triex_t   VARCHAR(20) AS (CONCAT(QUARTER(di),'º trimestre')) STORED,
  anotri    CHAR(7) AS (CONCAT(YEAR(di),'T',QUARTER(di))) STORED,
  semestre  TINYINT AS ((MONTH(di)-1) DIV 6 + 1) STORED,
  sem_inicio DATE AS (MAKEDATE(YEAR(di),1) + INTERVAL (MONTH(di)-1) DIV 6 * 6 MONTH) STORED,
  sem_fim   DATE AS (LAST_DAY(sem_inicio + INTERVAL 5 MONTH)) STORED,
  semex_t   VARCHAR(20) AS (CONCAT((MONTH(di)-1) DIV 6 + 1,'º semestre')) STORED,
  anosem    CHAR(7) AS (CONCAT(YEAR(di),'S',(MONTH(di)-1) DIV 6 + 1)) STORED,
  UNIQUE KEY uq_dimtempo_di (di),
  KEY ix_anomes (anomes), KEY ix_anobi (anobi), KEY ix_anotri (anotri), KEY ix_anosem (anosem)
) DEFAULT CHARSET=utf8mb4;

INSERT INTO DIMTEMPO (di)
WITH RECURSIVE m (d) AS (
  SELECT DATE '2010-01-01'
  UNION ALL SELECT d + INTERVAL 1 MONTH FROM m WHERE d < DATE '2026-11-01')
SELECT d FROM m;
