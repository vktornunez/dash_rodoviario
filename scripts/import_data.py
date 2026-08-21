"""
=============================================================================
PROJETO INTEGRADO III - SPRINT 1
Script de Carga e Tratamento de Dados (ETL) - CSV PRF 2025 -> PostgreSQL
Membro Responsável: Ramon (Banco de Dados / Product Owner)
=============================================================================
"""

import sys
import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "prf_db")
DB_USER = os.getenv("POSTGRES_USER", "prf_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "prf_pass")

CSV_FILE = os.path.join(os.path.dirname(__file__), "..", "acidentes2025_todas_causas_tipos.csv")

def parse_num(val):
    if pd.isna(val) or val == 'NA' or val == '':
        return None
    try:
        val_str = str(val).replace(',', '.')
        return float(val_str)
    except Exception:
        return None

def parse_int(val):
    num = parse_num(val)
    return int(num) if num is not None else 0

def clean_data():
    print(f"Lendo dataset: {CSV_FILE}...")
    if not os.path.exists(CSV_FILE):
        print(f"Erro: Arquivo {CSV_FILE} não encontrado!")
        return

    # Conectar ao banco PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    chunk_size = 50000
    total_ocorrencias = 0
    total_envolvidos = 0
    ocorrencias_processadas = set()

    for chunk in pd.read_csv(CSV_FILE, sep=';', encoding='latin1', chunksize=chunk_size, low_memory=False):
        # 1. Tratar Ocorrências (Deduplicadas por ID do Acidente)
        df_ocorrencias = chunk.drop_duplicates(subset=['id'])
        
        records_oc = []
        for idx, row in df_ocorrencias.iterrows():
            acidente_id = int(row['id'])
            if acidente_id in ocorrencias_processadas:
                continue
            ocorrencias_processadas.add(acidente_id)
            
            lat = parse_num(row.get('latitude'))
            lng = parse_num(row.get('longitude'))
            km = parse_num(row.get('km'))
            br = parse_int(row.get('br'))
            ordem = parse_int(row.get('ordem_tipo_acidente'))

            records_oc.append((
                acidente_id,
                str(row.get('data_inversa')),
                str(row.get('dia_semana')),
                str(row.get('horario')),
                str(row.get('uf')),
                br,
                km,
                str(row.get('municipio')),
                str(row.get('causa_principal')),
                str(row.get('causa_acidente')),
                ordem,
                str(row.get('tipo_acidente')),
                str(row.get('classificacao_acidente')),
                str(row.get('fase_dia')),
                str(row.get('sentido_via')),
                str(row.get('condicao_metereologica')),
                str(row.get('tipo_pista')),
                str(row.get('tracado_via')),
                str(row.get('uso_solo')),
                lat,
                lng,
                str(row.get('regional')),
                str(row.get('delegacia')),
                str(row.get('uop'))
            ))

        if records_oc:
            sql_oc = """
            INSERT INTO ocorrencia (
                id, data_inversa, dia_semana, horario, uf, br, km, municipio,
                causa_principal, causa_acidente, ordem_tipo_acidente, tipo_acidente,
                classificacao_acidente, fase_dia, sentido_via, condicao_metereologica,
                tipo_pista, tracado_via, uso_solo, latitude, longitude, regional, delegacia, uop
            ) VALUES %s ON CONFLICT (id) DO NOTHING;
            """
            execute_values(cursor, sql_oc, records_oc)
            total_ocorrencias += len(records_oc)

        # 2. Tratar Envolvidos (Granularidade da Pessoa)
        records_env = []
        for idx, row in chunk.iterrows():
            pesid = int(row['pesid']) if pd.notna(row.get('pesid')) else None
            id_oc = int(row['id']) if pd.notna(row.get('id')) else None
            
            if not pesid or not id_oc:
                continue

            records_env.append((
                pesid,
                id_oc,
                parse_int(row.get('id_veiculo')),
                str(row.get('tipo_veiculo')),
                str(row.get('marca')),
                parse_int(row.get('ano_fabricacao_veiculo')),
                str(row.get('tipo_envolvido')),
                str(row.get('estado_fisico')),
                parse_int(row.get('idade')),
                str(row.get('sexo')),
                parse_int(row.get('ilesos')),
                parse_int(row.get('feridos_leves')),
                parse_int(row.get('feridos_graves')),
                parse_int(row.get('mortos'))
            ))

        if records_env:
            sql_env = """
            INSERT INTO envolvido (
                pesid, id_ocorrencia, id_veiculo, tipo_veiculo, marca, ano_fabricacao_veiculo,
                tipo_envolvido, estado_fisico, idade, sexo, ilesos, feridos_leves, feridos_graves, mortos
            ) VALUES %s ON CONFLICT (pesid) DO NOTHING;
            """
            execute_values(cursor, sql_env, records_env)
            total_envolvidos += len(records_env)

        conn.commit()
        print(f"Status Carga: {total_ocorrencias} Ocorrências | {total_envolvidos} Envolvidos inseridos...")

    cursor.close()
    conn.close()
    print("ETL concluído com sucesso!")

if __name__ == '__main__':
    clean_data()
