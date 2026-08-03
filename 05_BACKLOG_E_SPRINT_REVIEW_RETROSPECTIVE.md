# Backlog, Sprint Review & Sprint Retrospective — Sprint 1
**Sistema**: Dashboard de Acidentes nas Rodovias Federais (PRF 2025)  
**Membro Responsável**: Victor (Scrum Master / Gerente de Projeto)

---

## 1. Product Backlog Atualizado

| ID | Estória de Usuário / Item de Backlog | Responsável |  | Status |
| :--- | :--- | :--- | :--- | :--- |
| **US01** | Modelagem relacional e scripts DDL desduplicando `ocorrencia` e `envolvido`. | Ramon |  | **Concluído** |
| **US02** | Criação de Views SQL para cálculo do Índice Comparativo de Risco (ICR). | Ramon |  | **Concluído** |
| **US03** | Script ETL em Python para ingestão limpa do CSV PRF 2025. | Ramon |  | **Concluído** |
| **US04** | Configuração do ambiente Docker e Docker Compose (Postgres + Backend API). | Petrus |  | **Concluído** |
| **US05** | Desenvolvimento da API REST em FastAPI com rotas de KPIs, gráficos e tabelas. | Petrus |  | **Concluído** |
| **US06** | Construção da interface gráfica do Dashboard com tema Dark Institucional PRF. | Victor |  | **Concluído** |
| **US07** | Integração do Mapa Interativo Leaflet com marcadores por UF e severidade. | Victor |  | **Concluído** |
| **US08** | Integração dos gráficos dinâmicos Chart.js (Evolução, Tipos, Causas, BRs). | Victor |  | **Concluído** |
| **US09** | Elaboração de toda a documentação arquitetural e de requisitos da Sprint 1. | Victor / Equipe |  | **Concluído** |


---

## 2. Sprint 1 Review (Revisão da Sprint)

- **Objetivo da Sprint**: Construir a fundação técnica e organizacional do projeto, contemplando requisitos, arquitetura, modelagem do banco de dados, protótipos e organização do backlog.
- **Resultado**: 100% dos 10 entregáveis previstos foram construídos com sucesso e validados conforme a Definição de Pronto (DoD).
- **Entregáveis Validados**:
  1. Documento de Requisitos (`01_DOCUMENTO_DE_REQUISITOS.md`)
  2. Documento de Arquitetura (`02_DOCUMENTO_DE_ARQUITETURA.md`)
  3. Modelo Conceitual (`03_MODELO_CONCEITUAL.md`)
  4. Modelo Lógico (`04_MODELO_LOGICO.md`)
  5. Modelo Físico (`database/init.sql`)
  6. Scripts SQL Iniciais & ETL (`database/init.sql`, `database/import_data.py`)
  7. Protótipo das Telas (`frontend/index.html`, `style.css`, `app.js`)
  8. Backlog Atualizado (`05_BACKLOG_E_SPRINT_REVIEW_RETROSPECTIVE.md`)
  9. GitHub Organizado (Estrutura modular sem conflitos)
  10. Sprint Review & Retrospective

---

## 3. Sprint 1 Retrospective (Retrospectiva)

### O que funcionou bem?
- **Divisão clara de papéis**: A separação de responsabilidades (Ramon em DB, Petrus em Backend, Victor em Frontend/Scrum) evitou sobreposições de código.
- **Resolução da regra de desduplicação**: A chave composta e separação em duas tabelas permitiu manter a integridade relacional sem perder os dados dos envolvidos.
- **Fallback resiliente na API**: O backend e o frontend operam com dados mock caso o banco de dados esteja subindo no Docker, garantindo testabilidade imediata.

### O que pode ser melhorado?
- Otimização no tempo de parse do arquivo CSV de 222MB no script ETL.
- Expansão dos testes unitários automatizados para endpoints da API.

### Plano de Ação para a Sprint 2:
1. Implementar filtros multi-seleção e exportação de relatórios em CSV/PDF.
2. Adicionar biblioteca `GeoJSON` para contornos vetoriais precisos dos estados brasileiros no mapa.
