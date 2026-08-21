"""
=============================================================================
PROJETO INTEGRADO III - SPRINT 1
API REST Backend - Dashboard de Acidentes nas Rodovias Federais (PRF 2025)
Membro Responsável: Petrus (Backend / Desenvolvedor)
=============================================================================
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
from scr.backend.config import settings
from scr.backend.database import get_db_connection

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="API REST para consumo do Dashboard de Acidentes Rodoviários da PRF 2025."
)

# Habilitar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# DADOS DE FALLBACK (CASO O BANCO DE DADOS AINDA NÃO TENHA SIDO CARREGADO)
# -----------------------------------------------------------------------------
MOCK_KPIS = {
    "total_acidentes": 45532,
    "total_mortos": 3593,
    "total_feridos": 62904,
    "total_feridos_graves": 14200,
    "total_feridos_leves": 48704,
    "total_ilesos": 32150,
    "indice_risco_total": 202399,
    "indice_risco_medio": 4.45
}

MOCK_EVOLUCAO_MENSAL = [
    {"mes_num": 1, "mes_nome": "Jan", "total_acidentes": 6420, "total_mortos": 510, "total_feridos": 8900},
    {"mes_num": 2, "mes_nome": "Fev", "total_acidentes": 6150, "total_mortos": 490, "total_feridos": 8450},
    {"mes_num": 3, "mes_nome": "Mar", "total_acidentes": 6780, "total_mortos": 530, "total_feridos": 9200},
    {"mes_num": 4, "mes_nome": "Abr", "total_acidentes": 6300, "total_mortos": 485, "total_feridos": 8600},
    {"mes_num": 5, "mes_nome": "Mai", "total_acidentes": 6600, "total_mortos": 525, "total_feridos": 9100},
    {"mes_num": 6, "mes_nome": "Jun", "total_acidentes": 6500, "total_mortos": 510, "total_feridos": 8950},
    {"mes_num": 7, "mes_nome": "Jul", "total_acidentes": 6782, "total_mortos": 543, "total_feridos": 9704}
]

MOCK_TIPOS_ACIDENTE = [
    {"tipo_acidente": "Colisão frontal", "total_ocorrencias": 12450, "percentual": 27.34},
    {"tipo_acidente": "Colisão traseira", "total_ocorrencias": 10210, "percentual": 22.42},
    {"tipo_acidente": "Saída de leito carroçável", "total_ocorrencias": 8150, "percentual": 17.90},
    {"tipo_acidente": "Tombamento", "total_ocorrencias": 5420, "percentual": 11.90},
    {"tipo_acidente": "Atropelamento de Pedestre", "total_ocorrencias": 4800, "percentual": 10.54},
    {"tipo_acidente": "Outros", "total_ocorrencias": 4502, "percentual": 9.90}
]

MOCK_CAUSAS_ACIDENTE = [
    {"causa_acidente": "Falta de atenção ao conduzir", "total_ocorrencias": 14205, "percentual": 31.20},
    {"causa_acidente": "Velocidade incompatível", "total_ocorrencias": 9560, "percentual": 21.00},
    {"causa_acidente": "Reação tardia ou ineficiente", "total_ocorrencias": 7280, "percentual": 16.00},
    {"causa_acidente": "Ingestão de álcool", "total_ocorrencias": 5010, "percentual": 11.00},
    {"causa_acidente": "Desobediência às normas de trânsito", "total_ocorrencias": 4800, "percentual": 10.54},
    {"causa_acidente": "Condutor dormiu ao volante", "total_ocorrencias": 4677, "percentual": 10.26}
]

MOCK_RISCO_UF = [
    {"uf": "MG", "total_acidentes": 6850, "total_mortos": 580, "icr_total": 29800, "icr_medio": 4.35, "lat_centroide": -18.5122, "lng_centroide": -44.5550},
    {"uf": "PR", "total_acidentes": 5920, "total_mortos": 490, "icr_total": 25100, "icr_medio": 4.24, "lat_centroide": -25.2521, "lng_centroide": -52.0215},
    {"uf": "SC", "total_acidentes": 5410, "total_mortos": 380, "icr_total": 21400, "icr_medio": 3.95, "lat_centroide": -27.2423, "lng_centroide": -50.2189},
    {"uf": "SP", "total_acidentes": 4890, "total_mortos": 410, "icr_total": 20800, "icr_medio": 4.25, "lat_centroide": -23.5505, "lng_centroide": -46.6333},
    {"uf": "BA", "total_acidentes": 3950, "total_mortos": 440, "icr_total": 19500, "icr_medio": 4.93, "lat_centroide": -12.9714, "lng_centroide": -38.5014},
    {"uf": "RJ", "total_acidentes": 3600, "total_mortos": 290, "icr_total": 14900, "icr_medio": 4.13, "lat_centroide": -22.9068, "lng_centroide": -43.1729},
    {"uf": "PE", "total_acidentes": 2800, "total_mortos": 250, "icr_total": 12100, "icr_medio": 4.32, "lat_centroide": -8.0476, "lng_centroide": -34.8770},
    {"uf": "CE", "total_acidentes": 2100, "total_mortos": 210, "icr_total": 9800, "icr_medio": 4.66, "lat_centroide": -3.7319, "lng_centroide": -38.5267}
]

MOCK_RODOVIAS_CRITICAS = [
    {"br": 116, "total_acidentes": 8420, "total_mortos": 710, "icr_total": 36500},
    {"br": 101, "total_acidentes": 7950, "total_mortos": 650, "icr_total": 33800},
    {"br": 381, "total_acidentes": 3920, "total_mortos": 340, "icr_total": 16900},
    {"br": 40, "total_acidentes": 3100, "total_mortos": 260, "icr_total": 13200},
    {"br": 277, "total_acidentes": 2850, "total_mortos": 220, "icr_total": 11800},
    {"br": 153, "total_acidentes": 2400, "total_mortos": 210, "icr_total": 10500},
    {"br": 262, "total_acidentes": 2100, "total_mortos": 180, "icr_total": 9100},
    {"br": 316, "total_acidentes": 1950, "total_mortos": 170, "icr_total": 8400},
    {"br": 230, "total_acidentes": 1800, "total_mortos": 150, "icr_total": 7700},
    {"br": 163, "total_acidentes": 1650, "total_mortos": 140, "icr_total": 7100}
]

# -----------------------------------------------------------------------------
# ROTAS DA API REST
# -----------------------------------------------------------------------------

@app.get("/health", tags=["Status"])
def health_check():
    conn = get_db_connection()
    db_status = "Connected" if conn else "Disconnected (Using Fallback Data)"
    if conn:
        conn.close()
    return {
        "status": "online",
        "system": settings.PROJECT_NAME,
        "database": db_status
    }

@app.get("/api/kpis", tags=["Dashboard"])
def get_kpis():
    """Retorna os Indicadores Chave de Desempenho (KPIs) nacionais."""
    conn = get_db_connection()
    if not conn:
        return MOCK_KPIS
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_kpis_nacionais LIMIT 1;")
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res if res else MOCK_KPIS
    except Exception:
        return MOCK_KPIS

@app.get("/api/evolucao-mensal", tags=["Dashboard"])
def get_evolucao_mensal():
    """Retorna a evolução temporal dos acidentes mês a mês em 2025."""
    conn = get_db_connection()
    if not conn:
        return MOCK_EVOLUCAO_MENSAL
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_evolucao_mensal;")
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res if res else MOCK_EVOLUCAO_MENSAL
    except Exception:
        return MOCK_EVOLUCAO_MENSAL

@app.get("/api/tipos-acidente", tags=["Dashboard"])
def get_tipos_acidente():
    """Retorna a distribuição percentual dos tipos/modalidades de acidentes."""
    conn = get_db_connection()
    if not conn:
        return MOCK_TIPOS_ACIDENTE
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_tipos_acidentes LIMIT 10;")
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res if res else MOCK_TIPOS_ACIDENTE
    except Exception:
        return MOCK_TIPOS_ACIDENTE

@app.get("/api/causas-acidente", tags=["Dashboard"])
def get_causas_acidente():
    """Retorna o ranking com as principais causas de acidentes."""
    conn = get_db_connection()
    if not conn:
        return MOCK_CAUSAS_ACIDENTE
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_causas_acidentes LIMIT 10;")
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res if res else MOCK_CAUSAS_ACIDENTE
    except Exception:
        return MOCK_CAUSAS_ACIDENTE

@app.get("/api/risco-estado", tags=["Dashboard"])
def get_risco_estado():
    """Retorna o Índice Comparativo de Risco (ICR) por Estado (UF)."""
    conn = get_db_connection()
    if not conn:
        return MOCK_RISCO_UF
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_indice_risco_uf;")
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res if res else MOCK_RISCO_UF
    except Exception:
        return MOCK_RISCO_UF

@app.get("/api/rodovias-criticas", tags=["Dashboard"])
def get_rodovias_criticas():
    """Retorna as Top 10 rodovias federais (BRs) com maior Índice Comparativo de Risco."""
    conn = get_db_connection()
    if not conn:
        return MOCK_RODOVIAS_CRITICAS
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vw_indice_risco_br LIMIT 10;")
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res if res else MOCK_RODOVIAS_CRITICAS
    except Exception:
        return MOCK_RODOVIAS_CRITICAS

@app.get("/api/ocorrencias", tags=["Tabela"])
def get_ocorrencias(
    uf: Optional[str] = None,
    br: Optional[int] = None,
    limit: int = 20,
    offset: int = 0
):
    """Consulta paginada da tabela de ocorrências com filtros opcionais por UF e BR."""
    conn = get_db_connection()
    if not conn:
        sample_list = [
            {"id": 652468, "data_inversa": "2025-01-01", "horario": "00:30:00", "uf": "PE", "br": 101, "km": 89.5, "municipio": "JABOATAO DOS GUARARAPES", "causa_acidente": "Reação tardia do condutor", "tipo_acidente": "Colisão traseira", "classificacao_acidente": "Com Vítimas Feridas"},
            {"id": 652469, "data_inversa": "2025-01-01", "horario": "01:15:00", "uf": "MG", "br": 116, "km": 420.0, "municipio": "GOVERNADOR VALADARES", "causa_acidente": "Velocidade incompatível", "tipo_acidente": "Colisão frontal", "classificacao_acidente": "Com Vítimas Fatais"},
            {"id": 652470, "data_inversa": "2025-01-01", "horario": "03:40:00", "uf": "PR", "br": 277, "km": 150.2, "municipio": "CURITIBA", "causa_acidente": "Falta de atenção ao conduzir", "tipo_acidente": "Saída de leito carroçável", "classificacao_acidente": "Sem Vítimas"},
            {"id": 652471, "data_inversa": "2025-01-02", "horario": "08:10:00", "uf": "SP", "br": 116, "km": 210.8, "municipio": "GUARULHOS", "causa_acidente": "Ingestão de álcool", "tipo_acidente": "Tombamento", "classificacao_acidente": "Com Vítimas Feridas"},
            {"id": 652472, "data_inversa": "2025-01-02", "horario": "14:25:00", "uf": "BA", "br": 101, "km": 305.0, "municipio": "FEIRA DE SANTANA", "causa_acidente": "Condutor dormiu ao volante", "tipo_acidente": "Colisão frontal", "classificacao_acidente": "Com Vítimas Fatais"}
        ]
        return {"total": len(sample_list), "data": sample_list}

    try:
        cursor = conn.cursor()
        query = "SELECT id, data_inversa, horario, uf, br, km, municipio, causa_acidente, tipo_acidente, classificacao_acidente FROM ocorrencia WHERE 1=1"
        params = []
        if uf:
            query += " AND uf = %s"
            params.append(uf.upper())
        if br:
            query += " AND br = %s"
            params.append(br)
        
        query += " ORDER BY data_inversa DESC, horario DESC LIMIT %s OFFSET %s;"
        params.extend([limit, offset])

        cursor.execute(query, params)
        data = cursor.fetchall()

        # Contar total filtrado
        count_query = "SELECT COUNT(*) as total FROM ocorrencia WHERE 1=1"
        count_params = []
        if uf:
            count_query += " AND uf = %s"
            count_params.append(uf.upper())
        if br:
            count_query += " AND br = %s"
            count_params.append(br)
            
        cursor.execute(count_query, count_params)
        total = cursor.fetchone()["total"]

        cursor.close()
        conn.close()
        return {"total": total, "data": data}
    except Exception:
        return {"total": 5, "data": []}
