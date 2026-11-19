USE sia;
CREATE OR REPLACE VIEW pa_ijui AS
SELECT dt.ano AS Ano, dt.mes AS Mes, dt.anobi AS AnoBimestre, dt.anotri AS AnoTrimestre,
       ca.fantasia AS Estabelecimento, pro.ip_dscr AS Procedimento, cb.ds_cbo AS Ocupacao,
       pa.PA_SEXO AS pa_sexo, pa.PA_IDADE AS pa_idade, pa.PA_CIDPRI AS pa_cidpri,
       cid.cd_descr AS Diagnostico,
       mun_est.ds_nome AS MunicipioEstabelecimento, mun_pac.ds_nome AS MunicipioPaciente,
       pa.PA_QTDPRO AS pa_qtdpro, pa.PA_QTDAPR AS pa_qtdapr,
       pa.PA_VALPRO AS pa_valpro, pa.PA_VALAPR AS pa_valapr,
       pa.PA_CODUNI AS pa_coduni, pa.PA_PROC_ID AS pa_proc_id, pa.PA_CBOCOD AS pa_cbocod,
       pa.PA_MUNPCN AS pa_munpcn, pa.PA_TPUPS AS pa_tpups, pa.PA_CMP AS pa_cmp,
       pa.PA_MVM AS pa_mvm, dt.anomes AS AnoMes
FROM pars2607 pa
LEFT JOIN cadgerrs      ca      ON pa.PA_CODUNI  = ca.cnes
LEFT JOIN procedimentos pro     ON pa.PA_PROC_ID = pro.ip_cod
LEFT JOIN cbo           cb      ON pa.PA_CBOCOD  = cb.cbo
LEFT JOIN (SELECT cd_cod, cd_descr FROM cid WHERE BINARY cd_cod = BINARY UPPER(cd_cod)) cid
                                ON pa.PA_CIDPRI  = cid.cd_cod
LEFT JOIN tb_municip    mun_est ON pa.PA_UFMUN   = mun_est.co_municip
LEFT JOIN tb_municip    mun_pac ON pa.PA_MUNPCN  = mun_pac.co_municip
LEFT JOIN DIMTEMPO      dt      ON pa.PA_CMP     = dt.anomes
WHERE pa.PA_UFMUN = '431020';
