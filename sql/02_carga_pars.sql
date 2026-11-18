-- Aula 1 - Passo 4: carga em lote do PARS (CSV gerado a partir do DBF).
-- Executar no cliente de linha de comando:  mysql --local-infile=1 < sql/02_carga_pars.sql
-- Ajuste o caminho do CSV conforme o seu ambiente.
USE sia;
TRUNCATE TABLE pars2607;
LOAD DATA LOCAL INFILE 'dados/PARS2607.csv' INTO TABLE pars2607
  CHARACTER SET latin1
  FIELDS TERMINATED BY ',' ENCLOSED BY '"'
  LINES TERMINATED BY '\r\n'
  IGNORE 1 ROWS;
