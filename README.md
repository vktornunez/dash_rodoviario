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

---

## Como Executar o Projeto com Docker

1. **Subir os containers do Banco e Backend**:
   ```bash
   docker-compose up -d --build
   ```
2. **Importar os dados do CSV no PostgreSQL (Opcional caso queira popular a base inteira)**:
   ```bash
   python database/import_data.py
   ```
3. **Abrir a Interface Web**:
   Basta abrir o arquivo `frontend/index.html` em qualquer navegador web ou servi-lo localmente (ex: via Live Server ou `python -m http.server` dentro da pasta `frontend`).

---

## Guia Simples de Comandos Git por Membro da Equipe

Para garantir que cada membro (Ramon, Petrus e Victor) suba sua parte do código para o repositório no GitHub sem gerar conflitos, siga este passo a passo simples.

### 1. Preparação Inicial (Executado por Todos)
Abra o terminal no seu computador e clone o repositório do projeto:
```bash
git clone https://github.com/SEU-USUARIO/PROJETO-INTEGRADO-III.git
cd PROJETO-INTEGRADO-III
```

---

### Fluxo do Ramon (Banco de Dados)
Como Ramon é responsável pela pasta `database/`:

1. Cria uma branch própria para suas alterações:
   ```bash
   git checkout -b feature/banco-de-dados
   ```
2. Adiciona os arquivos da sua pasta:
   ```bash
   git add database/
   ```
3. Faz o commit com uma mensagem clara:
   ```bash
   git commit -m "feat(database): adiciona DDL init.sql com views de risco ICR e script ETL"
   ```
4. Envia a branch para o GitHub:
   ```bash
   git push origin feature/banco-de-dados
   ```
5. No GitHub, abra um **Pull Request (PR)** para a branch `main`.

---

### Fluxo do Petrus (Backend / Docker)
Como Petrus é responsável pelas configurações Docker e pasta `backend/`:

1. Cria sua branch de trabalho:
   ```bash
   git checkout -b feature/backend-infra
   ```
2. Adiciona seus arquivos:
   ```bash
   git add docker-compose.yml Dockerfile backend/
   ```
3. Faz o commit:
   ```bash
   git commit -m "feat(backend): adiciona docker-compose, Dockerfile e rotas da API em FastAPI"
   ```
4. Envia para o GitHub:
   ```bash
   git push origin feature/backend-infra
   ```
5. No GitHub, abra o **Pull Request (PR)** para a branch `main`.

---

### Fluxo do Victor (Frontend / Documentação)
Como Victor é responsável pelas pastas `frontend/` e `docs/`:

1. Cria sua branch de trabalho:
   ```bash
   git checkout -b feature/frontend-docs
   ```
2. Adiciona seus arquivos:
   ```bash
   git add frontend/ docs/ README.md
   ```
3. Faz o commit:
   ```bash
   git commit -m "feat(frontend): adiciona dashboard interativo, mapa Leaflet e documentacao da Sprint 1"
   ```
4. Envia para o GitHub:
   ```bash
   git push origin feature/frontend-docs
   ```
5. No GitHub, abra o **Pull Request (PR)** para a branch `main`.

---

### Resumo do Fluxo de Trabalho sem Conflitos:
- **`git clone`**: Baixa o projeto para a sua máquina.
- **`git checkout -b <nome>`**: Cria a sua "área individual de trabalho" (branch).
- **`git add <pasta>`**: Prepara apenas os arquivos sob sua responsabilidade.
- **`git commit -m "mensagem"`**: Salva uma versão do seu trabalho com um comentário explicativo.
- **`git push origin <nome>`**: Envia sua parte pronta para a nuvem no GitHub para revisão!
