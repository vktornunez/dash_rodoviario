-- =============================================================================
-- PROJETO INTEGRADO III - SPRINT 1
-- Sistema: Dashboard de Acidentes nas Rodovias Federais (PRF 2025)
-- Membro Responsável: Ramon (Banco de Dados / Product Owner)
-- Script DDL: Criação do Esquema, Tabelas, Índices, Views de Risco (ICR) e Triggers
-- =============================================================================

-- 1. CRIAÇÃO DAS TABELAS COM GRANULARIDADE SEPARADA

-- Tabela 1: Ocorrencia (Granularidade: Evento de Acidente - Único por ID)
CREATE TABLE IF NOT EXISTS ocorrencia (
    id BIGINT PRIMARY KEY,
    data_inversa DATE NOT NULL,
    dia_semana VARCHAR(20),
    horario TIME,
    uf VARCHAR(2) NOT NULL,
    br INT,
    km NUMERIC(8,2),
    municipio VARCHAR(100),
    causa_principal VARCHAR(255),
    causa_acidente TEXT,
    ordem_tipo_acidente INT,
    tipo_acidente TEXT,
    classificacao_acidente VARCHAR(255),
    fase_dia VARCHAR(30),
    sentido_via VARCHAR(30),
    condicao_metereologica VARCHAR(255),
    tipo_pista VARCHAR(30),
    tracado_via VARCHAR(255),
    uso_solo VARCHAR(10),
    latitude NUMERIC(10,8),
    longitude NUMERIC(11,8),
    regional VARCHAR(255),
    delegacia VARCHAR(255),
    uop VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela 2: Envolvido (Granularidade: Pessoas/Veículos Envolvidos no Acidente)
-- Regra de Negócio: Múltiplos envolvidos compartilham o mesmo id_ocorrencia
CREATE TABLE IF NOT EXISTS envolvido (
    pesid BIGINT PRIMARY KEY,
    id_ocorrencia BIGINT NOT NULL REFERENCES ocorrencia(id) ON DELETE CASCADE,
    id_veiculo BIGINT,
    tipo_veiculo VARCHAR(50),
    marca VARCHAR(100),
    ano_fabricacao_veiculo INT,
    tipo_envolvido VARCHAR(255),
    estado_fisico VARCHAR(50),
    idade INT,
    sexo VARCHAR(20),
    ilesos INT DEFAULT 0,
    feridos_leves INT DEFAULT 0,
    feridos_graves INT DEFAULT 0,
    mortos INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CRIAÇÃO DE ÍNDICES PARA ALTA PERFORMANCE

CREATE INDEX IF NOT EXISTS idx_ocorrencia_uf ON ocorrencia(uf);
CREATE INDEX IF NOT EXISTS idx_ocorrencia_br ON ocorrencia(br);
CREATE INDEX IF NOT EXISTS idx_ocorrencia_data ON ocorrencia(data_inversa);
CREATE INDEX IF NOT EXISTS idx_ocorrencia_uf_br ON ocorrencia(uf, br);
CREATE INDEX IF NOT EXISTS idx_envolvido_ocorrencia ON envolvido(id_ocorrencia);
CREATE INDEX IF NOT EXISTS idx_envolvido_estado_fisico ON envolvido(estado_fisico);

-- 3. VIEWS DE ANÁLISE DE RISCO E KPIS (ÍNDICE COMPARATIVO DE RISCO - ICR)
-- Fórmula ICR: (0 * Ilesos) + (1 * Feridos Leves) + (5 * Feridos Graves) + (15 * Mortos)

-- View 1: KPIs Nacionais Consolidados
CREATE OR REPLACE VIEW vw_kpis_nacionais AS
SELECT 
    COUNT(DISTINCT o.id) AS total_acidentes,
    COALESCE(SUM(e.mortos), 0) AS total_mortos,
    COALESCE(SUM(e.feridos_graves), 0) AS total_feridos_graves,
    COALESCE(SUM(e.feridos_leves), 0) AS total_feridos_leves,
    COALESCE(SUM(e.ilesos), 0) AS total_ilesos,
    COALESCE(SUM(e.feridos_leves + e.feridos_graves), 0) AS total_feridos,
    SUM((e.ilesos * 0) + (e.feridos_leves * 1) + (e.feridos_graves * 5) + (e.mortos * 15)) AS indice_risco_total,
    ROUND(
        SUM((e.ilesos * 0) + (e.feridos_leves * 1) + (e.feridos_graves * 5) + (e.mortos * 15))::NUMERIC / 
        NULLIF(COUNT(DISTINCT o.id), 0), 2
    ) AS indice_risco_medio
FROM ocorrencia o
LEFT JOIN envolvido e ON o.id = e.id_ocorrencia;

-- View 2: Ranking de Risco por Estado (UF)
CREATE OR REPLACE VIEW vw_indice_risco_uf AS
SELECT 
    o.uf,
    COUNT(DISTINCT o.id) AS total_acidentes,
    COALESCE(SUM(e.mortos), 0) AS total_mortos,
    COALESCE(SUM(e.feridos_graves), 0) AS total_feridos_graves,
    COALESCE(SUM(e.feridos_leves), 0) AS total_feridos_leves,
    SUM((e.ilesos * 0) + (e.feridos_leves * 1) + (e.feridos_graves * 5) + (e.mortos * 15)) AS icr_total,
    ROUND(
        SUM((e.ilesos * 0) + (e.feridos_leves * 1) + (e.feridos_graves * 5) + (e.mortos * 15))::NUMERIC / 
        NULLIF(COUNT(DISTINCT o.id), 0), 2
    ) AS icr_medio,
    AVG(o.latitude) AS lat_centroide,
    AVG(o.longitude) AS lng_centroide
FROM ocorrencia o
LEFT JOIN envolvido e ON o.id = e.id_ocorrencia
GROUP BY o.uf
ORDER BY icr_total DESC;

-- View 3: Ranking de Rodovias Críticas (Top Rodovias Federais - BRs)
CREATE OR REPLACE VIEW vw_indice_risco_br AS
SELECT 
    o.br,
    COUNT(DISTINCT o.id) AS total_acidentes,
    COALESCE(SUM(e.mortos), 0) AS total_mortos,
    COALESCE(SUM(e.feridos_graves), 0) AS total_feridos_graves,
    COALESCE(SUM(e.feridos_leves), 0) AS total_feridos_leves,
    SUM((e.ilesos * 0) + (e.feridos_leves * 1) + (e.feridos_graves * 5) + (e.mortos * 15)) AS icr_total
FROM ocorrencia o
LEFT JOIN envolvido e ON o.id = e.id_ocorrencia
WHERE o.br IS NOT NULL
GROUP BY o.br
ORDER BY icr_total DESC;

-- View 4: Evolução Mensal dos Acidentes (Jan a Dez 2025)
CREATE OR REPLACE VIEW vw_evolucao_mensal AS
SELECT 
    EXTRACT(MONTH FROM o.data_inversa) AS mes_num,
    TO_CHAR(o.data_inversa, 'Mon') AS mes_nome,
    COUNT(DISTINCT o.id) AS total_acidentes,
    COALESCE(SUM(e.mortos), 0) AS total_mortos,
    COALESCE(SUM(e.feridos_leves + e.feridos_graves), 0) AS total_feridos
FROM ocorrencia o
LEFT JOIN envolvido e ON o.id = e.id_ocorrencia
GROUP BY EXTRACT(MONTH FROM o.data_inversa), TO_CHAR(o.data_inversa, 'Mon')
ORDER BY mes_num;

-- View 5: Principais Causas de Acidentes
CREATE OR REPLACE VIEW vw_causas_acidentes AS
SELECT 
    o.causa_acidente,
    COUNT(DISTINCT o.id) AS total_ocorrencias,
    ROUND((COUNT(DISTINCT o.id)::NUMERIC / (SELECT COUNT(*) FROM ocorrencia)) * 100, 2) AS percentual
FROM ocorrencia o
WHERE o.causa_acidente IS NOT NULL AND o.causa_acidente != ''
GROUP BY o.causa_acidente
ORDER BY total_ocorrencias DESC;

-- View 6: Tipos de Acidentes (Modalidades)
CREATE OR REPLACE VIEW vw_tipos_acidentes AS
SELECT 
    o.tipo_acidente,
    COUNT(DISTINCT o.id) AS total_ocorrencias,
    ROUND((COUNT(DISTINCT o.id)::NUMERIC / (SELECT COUNT(*) FROM ocorrencia)) * 100, 2) AS percentual
FROM ocorrencia o
WHERE o.tipo_acidente IS NOT NULL AND o.tipo_acidente != ''
GROUP BY o.tipo_acidente
ORDER BY total_ocorrencias DESC;
