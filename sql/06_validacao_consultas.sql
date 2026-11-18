-- Aula 1 - Passos 5 e 6: validação e consultas de demonstração.
USE sia;

-- Estrutura e contagem de registros
SHOW TABLES;
DESCRIBE pars2607;
SELECT COUNT(*) AS registros_pars2607 FROM pars2607;                       -- 4.532.294 (= linhas do CSV)
SELECT COUNT(*) AS registros_ijui FROM pars2607 WHERE PA_UFMUN = '431020';
SELECT 'cadgerrs' t, COUNT(*) n FROM cadgerrs UNION ALL SELECT 'cbo', COUNT(*) FROM cbo
UNION ALL SELECT 'cid', COUNT(*) FROM cid UNION ALL SELECT 'procedimentos', COUNT(*) FROM procedimentos
UNION ALL SELECT 'tb_municip', COUNT(*) FROM tb_municip UNION ALL SELECT 'DIMTEMPO', COUNT(*) FROM DIMTEMPO;

-- Integridade: registros de Ijuí sem correspondência nas tabelas descritivas
SELECT SUM(ca.cnes IS NULL) sem_estab, SUM(pro.ip_cod IS NULL) sem_proc,
       SUM(cb.cbo IS NULL) sem_cbo, SUM(dt.anomes IS NULL) sem_tempo
FROM pars2607 pa
LEFT JOIN cadgerrs ca ON pa.PA_CODUNI = ca.cnes
LEFT JOIN procedimentos pro ON pa.PA_PROC_ID = pro.ip_cod
LEFT JOIN cbo cb ON pa.PA_CBOCOD = cb.cbo
LEFT JOIN DIMTEMPO dt ON pa.PA_MVM = dt.anomes
WHERE pa.PA_UFMUN = '431020';

-- Consultas de demonstração
SELECT Estabelecimento, SUM(pa_qtdapr) AS qtd_aprovada, SUM(pa_valapr) AS valor_aprovado
FROM pa_ijui GROUP BY Estabelecimento ORDER BY qtd_aprovada DESC LIMIT 10;

SELECT Procedimento, SUM(pa_qtdapr) AS qtd FROM pa_ijui GROUP BY Procedimento ORDER BY qtd DESC LIMIT 10;

SELECT MunicipioPaciente, COUNT(*) AS registros FROM pa_ijui GROUP BY MunicipioPaciente ORDER BY registros DESC LIMIT 10;
