# Modelo Lógico do Banco de Dados — Sprint 1
**Sistema**: Dashboard de Acidentes nas Rodovias Federais (PRF 2025)  
**Membro Responsável**: Ramon (Banco de Dados / Product Owner)

---

## 1. Esquema Relacional Lógico

### Tabela `ocorrencia`
| Coluna | Tipo de Dado | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `id` | `BIGINT` | `PRIMARY KEY` | ID único da ocorrência |
| `data_inversa` | `DATE` | `NOT NULL` | Data do acidente (AAAA-MM-DD) |
| `dia_semana` | `VARCHAR(20)` | | Dia da semana |
| `horario` | `TIME` | | Horário da ocorrência |
| `uf` | `VARCHAR(2)` | `NOT NULL` | Unidade Federativa |
| `br` | `INT` | | Número da Rodovia Federal |
| `km` | `NUMERIC(8,2)` | | Quilômetro da rodovia |
| `municipio` | `VARCHAR(100)` | | Nome do município |
| `causa_principal` | `VARCHAR(10)` | | Causa principal (Sim/Não) |
| `causa_acidente` | `TEXT` | | Descrição da causa do acidente |
| `ordem_tipo_acidente` | `INT` | | Ordem de relevância do tipo |
| `tipo_acidente` | `TEXT` | | Modalidade do acidente |
| `classificacao_acidente` | `VARCHAR(50)` | | Com Vítimas Fatais, Feridas, Sem Vítimas |
| `fase_dia` | `VARCHAR(30)` | | Plena Noite, Dia, Alvorada, etc. |
| `sentido_via` | `VARCHAR(30)` | | Crescente ou Decrescente |
| `condicao_metereologica` | `VARCHAR(50)` | | Céu Claro, Chuva, Sol, etc. |
| `tipo_pista` | `VARCHAR(30)` | | Simples, Dupla, Múltipla |
| `tracado_via` | `VARCHAR(50)` | | Reta, Curva, Interseção |
| `uso_solo` | `VARCHAR(10)` | | Urbano ou Rural (Sim/Não) |
| `latitude` | `NUMERIC(10,8)` | | Coordenada Geográfica (Latitude) |
| `longitude` | `NUMERIC(11,8)` | | Coordenada Geográfica (Longitude) |
| `regional` | `VARCHAR(50)` | | Superintendência Regional PRF |
| `delegacia` | `VARCHAR(50)` | | Delegacia PRF responsável |
| `uop` | `VARCHAR(50)` | | Unidade Operacional PRF |

### Tabela `envolvido`
| Coluna | Tipo de Dado | Restrições | Descrição |
| :--- | :--- | :--- | :--- |
| `pesid` | `BIGINT` | `PRIMARY KEY` | ID único da pessoa |
| `id_ocorrencia` | `BIGINT` | `FK -> ocorrencia(id)` | ID do acidente (FK) |
| `id_veiculo` | `BIGINT` | | ID do veículo envolvido |
| `tipo_veiculo` | `VARCHAR(50)` | | Automóvel, Motocicleta, Caminhão, etc. |
| `marca` | `VARCHAR(100)` | | Marca/Modelo do veículo |
| `ano_fabricacao_veiculo`| `INT` | | Ano de fabricação |
| `tipo_envolvido` | `VARCHAR(50)` | | Condutor, Passageiro, Pedestre |
| `estado_fisico` | `VARCHAR(50)` | | Ileso, Lesões Leves, Lesões Graves, Morto |
| `idade` | `INT` | | Idade da pessoa |
| `sexo` | `VARCHAR(20)` | | Sexo (Masculino, Feminino, Não Informado) |
| `ilesos` | `INT` | `DEFAULT 0` | 1 se ileso, senão 0 |
| `feridos_leves` | `INT` | `DEFAULT 0` | 1 se ferido leve, senão 0 |
| `feridos_graves` | `INT` | `DEFAULT 0` | 1 se ferido grave, senão 0 |
| `mortos` | `INT` | `DEFAULT 0` | 1 se morto, senão 0 |

---

## 2. Regra do Índice Comparativo de Risco (ICR)
$$ICR = (0 \times ilesos) + (1 \times feridos\_leves) + (5 \times feridos\_graves) + (15 \times mortos)$$
Essa fórmula é calculada em nível de agregação por UF e por Rodovia (BR) através das Views SQL `vw_indice_risco_uf` e `vw_indice_risco_br`.
