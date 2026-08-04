# Documento de Requisitos — Sprint 1
**Sistema**: Dashboard de Acidentes nas Rodovias Federais (PRF 2025)  
**Projeto Integrado III — UFCA**

---

## 1. Escopo do Sistema
O sistema tem como objetivo coletar, processar e apresentar de forma analítica e interativa os dados oficiais de acidentes rodoviários federais no Brasil registrados pela Polícia Rodoviária Federal (PRF) no ano de 2025. O escopo é estritamente nacional.

---

## 2. Requisitos Funcionais (RF)

| ID | Descrição do Requisito Funcional | Prioridade | Atribuição |
| :--- | :--- | :--- | :--- |
| **RF01** | **Consolidação de KPIs Nacionais**: Exibir total de acidentes, vítimas fatais, feridos graves, feridos leves e o Índice Comparativo de Risco (ICR) acumulado. | Alta | Backend / Frontend |
| **RF02** | **Filtros Globais**: Permitir a filtragem dinâmica dos dados por Estado (UF) e por Rodovia Federal (BR). | Alta | Frontend / Backend |
| **RF03** | **Análise Temporal Mensal**: Exibir gráfico de linha/área da evolução de acidentes e vítimas fatais mês a mês em 2025. | Média | Frontend / Backend |
| **RF04** | **Classificação por Tipo de Acidente**: Exibir gráfico de rosca demonstrando as modalidades mais frequentes (ex: colisão frontal, traseira, tombamento). | Média | Frontend / Backend |
| **RF05** | **Ranking de Causas**: Apresentar em gráfico de barras as principais causas raiz dos acidentes (ex: falta de atenção, velocidade). | Média | Frontend / Backend |
| **RF06** | **Top 10 Rodovias Críticas**: Exibir o ranking das 10 BRs mais perigosas calculadas pelo ICR. | Alta | Banco / Backend |
| **RF07** | **Mapa Interativo de Risco (Leaflet)**: Apresentar mapa nacional com marcadores geolocalizados por estado (UF) coloridos de acordo com o nível de severidade/ICR. | Alta | Frontend |
| **RF08** | **Tabela Detalhada com Paginador**: Exibir listagem detalhada de ocorrências com busca textual, paginação e destaques visuais por gravidade. | Média | Frontend / Backend |
| **RF09** | **Cálculo do Índice Comparativo de Risco (ICR)**: Calcular o ICR via View SQL aplicando a fórmula: $(0 \times \text{ilesos}) + (1 \times \text{leves}) + (5 \times \text{graves}) + (15 \times \text{mortos})$. | Alta | Banco de Dados |
| **RF10** | **Tratamento de Duplicatas por Pessoa**: Desduplicar acidentes em nível de `ocorrencia` mantendo múltiplos registros de `envolvido` sob o mesmo `id` do acidente. | Alta | Banco de Dados |

---

## 3. Requisitos Não Funcionais (RNF)

| ID | Descrição do Requisito Não Funcional | Categoria |
| :--- | :--- | :--- |
| **RNF01** | **Desempenho**: Resposta das APIs em menos de 2 segundos para consultas com filtros. | Desempenho |
| **RNF02** | **Usabilidade & Estética**: Interface moderna com tema Dark Institucional PRF, responsiva e acessível. | Usabilidade |
| **RNF03** | **Arquitetura Containerizada**: Utilização do Docker e Docker Compose para orquestração de banco e API. | Infraestrutura |
| **RNF04** | **Compatibilidade**: Suporte aos principais navegadores web modernos (Chrome, Firefox, Edge, Safari). | Compatibilidade |
| **RNF05** | **Disponibilidade**: Fallback seguro para exibição de dados caso o serviço PostgreSQL esteja inicializando. | Confiabilidade |

---

## 4. Casos de Uso (UC)

### UC01 — Visualizar Dashboard Nacional
- **Ator**: Usuário / Analista de Trânsito PRF
- **Fluxo Principal**:
  1. O usuário acessa o sistema via navegador.
  2. O sistema consome os endpoints `/api/kpis`, `/api/evolucao-mensal`, `/api/risco-estado`.
  3. O dashboard renderiza os 4 cards de KPI, o mapa Leaflet e os gráficos estatísticos.

### UC02 — Filtrar Ocorrências por UF ou Rodovia
- **Ator**: Usuário
- **Fluxo Principal**:
  1. O usuário seleciona o estado "PE" ou digita a rodovia "101".
  2. Clica no botão "Filtrar Dados".
  3. O sistema atualiza a tabela de ocorrências e os rankings mantendo o filtro ativo.
