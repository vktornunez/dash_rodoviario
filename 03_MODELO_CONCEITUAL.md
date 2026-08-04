# Modelo Conceitual do Banco de Dados — Sprint 1
**Sistema**: Dashboard de Acidentes nas Rodovias Federais (PRF 2025)  
**Membro Responsável**: Ramon (Banco de Dados / Product Owner)

---

## 1. Descrição do Modelo Entidade-Relacionamento (DER)

O modelo conceitual resolve a regra de negócio crítica onde o arquivo CSV da PRF registra cada pessoa envolvida no acidente, repetindo o identificador do acidente `id`.

Para evitar anomalias de redundância e desduplicar a base, o modelo divide a granularidade em duas entidades fundamentais:

1. **`OCORRENCIA`**: Representa o evento do acidente em si (data, hora, rodovia, município, causas, condições meteorológicas, localização geográfica).
2. **`ENVOLVIDO`**: Representa o indivíduo envolvido no acidente (condutor, passageiro, pedestre), sua condição física (ileso, ferido leve, ferido grave, morto) e o veículo associado.

---

## 2. Diagrama Entidade-Relacionamento (Mermaid ER)

```mermaid
erDiagram
    OCORRENCIA ||--|{ ENVOLVIDO : "possui / envolve"
    
    OCORRENCIA {
        bigint id PK "Identificador Único do Acidente"
        date data_inversa "Data da Ocorrência"
        time horario "Horário"
        string uf "Estado"
        int br "Rodovia Federal"
        numeric km "Quilômetro"
        string municipio "Município"
        string causa_principal "Causa Principal (Sim/Não)"
        string causa_acidente "Descrição da Causa"
        string tipo_acidente "Modalidade / Tipo"
        string classificacao_acidente "Classificação de Vítimas"
        string fase_dia "Fase do Dia"
        numeric latitude "Latitude"
        numeric longitude "Longitude"
    }

    ENVOLVIDO {
        bigint pesid PK "Identificador Único da Pessoa"
        bigint id_ocorrencia FK "Chave Estrangeira do Acidente"
        bigint id_veiculo "Identificador do Veículo"
        string tipo_veiculo "Tipo do Veículo"
        string tipo_envolvido "Papel (Condutor/Passageiro/Pedestre)"
        string estado_fisico "Estado Físico"
        int idade "Idade"
        string sexo "Sexo"
        int ilesos "Indicador Ileso (0/1)"
        int feridos_leves "Indicador Ferido Leve (0/1)"
        int feridos_graves "Indicador Ferido Grave (0/1)"
        int mortos "Indicador Morto (0/1)"
    }
```

---

## 3. Regra de Negócio: Cardinalidade
- **Relacionamento**: Uma `OCORRENCIA` pode ter 1 ou vários (`1:N`) `ENVOLVIDOS`. Cada `ENVOLVIDO` pertence obrigatoriamente a exatamente 1 (`1:1`) `OCORRENCIA`.
