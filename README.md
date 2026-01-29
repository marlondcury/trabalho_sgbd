# Análise de Eficiência do Gasto Público - Alegre/ES 

Projeto de Business Intelligence e Engenharia de Dados desenvolvido como requisito da disciplina de Gerenciamento de Banco de Dados (2025/2). O objetivo é estruturar um Data Mart para análise histórica (10 anos) das despesas públicas municipais.

##  Objetivo do Projeto

Construir um Sistema de Apoio à Decisão (SAD) capaz de integrar dados financeiros da Prefeitura Municipal de Alegre com dados demográficos do IBGE, permitindo análises de evolução de gastos, custo *per capita* e distribuição orçamentária por função de governo.

##  Arquitetura e Tecnologias

O projeto segue uma arquitetura de ETL (Extract, Transform, Load) clássica, alimentando um Data Mart em modelo Star Schema (Estrela).

* **Linguagem:** Python 3.10+
* **Bibliotecas:** Pandas, Requests, XML.etree, JSON, SQLite3.
* **Fontes de Dados:**
    * API do Portal da Transparência de Alegre (Despesas/Pagamentos).
    * API do SIDRA - IBGE (Estimativas Populacionais - Tabela 6579).
* **Armazenamento:** SQLite (Data Mart local).

##  Pipeline de ETL

O processo foi dividido em três etapas modulares para garantir a rastreabilidade e facilidade de manutenção:

### 1. Extração (`etl_1_extracao.ipynb`)
Responsável por iterar sobre a API da transparência (período 2015-2025).
* **Desafio:** A API retorna um XML onde o conteúdo real é uma string JSON encapsulada.
* **Solução:** Implementação de um parser híbrido (XML + JSON) para estruturar os dados brutos em DataFrames.

## Como Executar


##  Próximos Passos

* Conexão do Data Mart (`.db`) ao Microsoft Power BI.
* Desenvolvimento de Dashboards interativos (Análise Temporal e Por Secretaria).


---
