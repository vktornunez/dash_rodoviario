# Dashboard de Acidentes nas Rodovias Federais — PRF 2025
> **Projeto Integrado III — UFCA (Universidade Federal do Cariri)**  
> **Sprint 1: Fundação Técnica, Modelagem de Banco, API REST, Frontend e Docker**

---

## Visão Geral do Projeto
Este projeto entrega o **Dashboard Analítico e Interativo de Acidentes nas Rodovias Federais Brasileiras (PRF 2025)**. O escopo abrange a análise de dados em escala nacional a partir da base oficial de dados abertos da Polícia Rodoviária Federal (`acidentes2025_todas_causas_tipos.csv`).

O painel contempla:
- **4 KPIs Nacionais**: Total de acidentes, vítimas fatais, feridos (leves/graves) e o Índice Comparativo de Risco (ICR).
- **Mapa Interativo (Leaflet)**: Risco por Estado (UF) com coordenadas geográficas.
- **Gráficos Dinâmicos (Chart.js)**: Evolução mensal, modalidades/tipos de acidente, causas principais e ranking das Top 10 BRs mais perigosas.
- **Tabela Paginada de Ocorrências**: Filtros por estado e rodovia, busca por texto e destaque visual de severidade.

---

## Estrutura da Equipe e Responsabilidades da Sprint 1

### 1. Ramon (Banco de Dados / Product Owner)
- **Atribuições**: Modelagem relacional relacional no PostgreSQL e desduplicação dos dados.
- **Regra de Negócio Implementada**: Separou a granularidade criando a tabela `ocorrencia` (nível de evento) e a tabela `envolvido` (nível individual). Trata a regra de que o mesmo `id` de acidente possui múltiplos envolvidos (`pesid`).
- **Arquivos Criados**:
  - `database/init.sql`: Script DDL com tabelas, chaves primárias/estrangeiras, índices e Views com cálculo do **Índice Comparativo de Risco (ICR)**.
  - `database/import_data.py`: Script ETL em Python para carga limpa do arquivo CSV de 222MB.

### 2. Petrus (Backend / Desenvolvedor)
- **Atribuições**: Configuração da infraestrutura containerizada e API REST base.
- **Tecnologias**: Python 3.11, FastAPI, Uvicorn e Docker Compose.
- **Arquivos Criados**:
  - `docker-compose.yml`: Orquestração do PostgreSQL 15 e container da API Backend.
  - `Dockerfile`: Imagem otimizada para o serviço Python FastAPI.
  - `backend/requirements.txt`: Dependências do projeto.
  - `backend/config.py` & `backend/database.py`: Conectividade e configurações.
  - `backend/main.py`: Estrutura da API REST com rotas `/api/kpis`, `/api/evolucao-mensal`, `/api/tipos-acidente`, `/api/causas-acidente`, `/api/risco-estado`, `/api/rodovias-criticas` e `/api/ocorrencias`.

### 3. Victor (Frontend / Scrum Master / Gerente de Projeto)
- **Atribuições**: Interface web responsiva e organização da documentação do projeto.
- **Tecnologias**: HTML5, CSS3 (Design Dark Institucional PRF), JavaScript ES6+, Leaflet.js e Chart.js.
- **Arquivos Criados**:
  - `frontend/index.html`: Layout moderno com cards de KPI, mapa, gráficos e tabela.
  - `frontend/style.css`: Paleta Dark Institucional PRF (`#0b132b`, `#ffb703`, `#3a86ef`, `#e63946`), glassmorphism e animações.
  - `frontend/app.js`: Chamadas `fetch` assíncronas para a API backend.
  - `docs/*`: Todos os 10 documentos e diagramas exigidos na Sprint 1.

---

## Estrutura de Pastas do Repositório

```
PROJETO INTEGRADO III/
├── docker-compose.yml              # Containerização Docker (Postgres + FastAPI)
├── Dockerfile                      # Imagem do Backend FastAPI
├── README.md                       # Documentação principal e tutorial Git
├── acidentes2025_todas_causas_tipos.csv  # Base oficial da PRF 2025 (222MB)
├── database/                       # [Ramon] Banco de Dados
│   ├── init.sql                    # DDL, Tabelas, Índices e Views ICR
│   └── import_data.py              # Script ETL de carga do CSV
├── backend/                        # [Petrus] API REST Python FastAPI
│   ├── requirements.txt            # Dependências Python
│   ├── config.py                   # Configurações globais
│   ├── database.py                 # Conexão PostgreSQL
│   └── main.py                     # Rotas da API REST
├── frontend/                       # [Victor] Interface do Dashboard
│   ├── index.html                  # HTML5 Semântico
│   ├── style.css                   # CSS Dark Institucional
│   └── app.js                      # Consumo da API e Gráficos/Mapa
└── docs/                           # Documentação Completa da Sprint 1
    ├── 01_DOCUMENTO_DE_REQUISITOS.md
    ├── 02_DOCUMENTO_DE_ARQUITETURA.md
    ├── 03_MODELO_CONCEITUAL.md
    ├── 04_MODELO_LOGICO.md
    └── 05_BACKLOG_E_SPRINT_REVIEW_RETROSPECTIVE.md
```




