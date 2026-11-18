-- Índices nas chaves usadas nos JOINs da VIEW (sem eles cada JOIN varre a tabela inteira).
USE sia;
ALTER TABLE pars2607     ADD INDEX idx_coduni (PA_CODUNI), ADD INDEX idx_cbo (PA_CBOCOD),
                         ADD INDEX idx_cidpri (PA_CIDPRI), ADD INDEX idx_munpcn (PA_MUNPCN),
                         ADD INDEX idx_mvm (PA_MVM);
-- (idx_ufmun e idx_proc já existem)
ALTER TABLE cadgerrs     ADD INDEX idx_cnes (cnes);
ALTER TABLE procedimentos ADD INDEX idx_ip_cod (ip_cod);
ALTER TABLE cbo          ADD INDEX idx_cbo (cbo);
ALTER TABLE cid          ADD INDEX idx_cd_cod (cd_cod);
ALTER TABLE tb_municip   ADD INDEX idx_co_municip (co_municip);
