# Automotive Data Platform

Pipeline de dados de veículos que consome a API VT3, aplica validações e transforma os registros em dados prontos para análise. O projeto usa uma arquitetura em camadas inspirada no padrão Medallion:

```text
API VT3 -> Bronze (JSON bruto) -> Data Quality -> Silver (Parquet) -> Gold (métricas JSON)
```

## Objetivos

- Extrair veículos da API por meio de um cliente HTTP configurável.
- Preservar a resposta original na camada Bronze.
- Identificar registros inválidos antes da transformação.
- Padronizar os nomes dos campos para consumo analítico.
- Gerar métricas agregadas por marca, combustível, câmbio e condição, além de médias de preço, quilometragem, visualizações e diferença para a FIPE.

## Requisitos

- Python 3.10 ou superior
- Acesso à API VT3
- `API_BASE_URL` configurada no ambiente

## Instalação

Clone o repositório, crie um ambiente virtual e instale as dependências:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```env
API_BASE_URL=https://seu-endpoint-da-api
```

O cliente adiciona `/cars` à URL base e faz requisições com paginação e limite de registros.

## Execução

Para executar o fluxo principal:

```bash
python -m src.pipeline.cars
```

O pipeline executa as etapas de ingestão, armazenamento Bronze, qualidade, transformação, armazenamento Silver, carregamento da Silver, analytics e armazenamento Gold. Cada execução deve ser identificada por um `run_id`, usado para separar os artefatos em `data/bronze`, `data/silver` e `data/gold`.

As etapas também possuem pontos de entrada próprios para inspeção isolada:

```bash
python -m src.ingestion.cars
python -m src.quality.cars
```

Esses comandos dependem de `API_BASE_URL` e fazem uma chamada real à API.

## Camadas de dados

| Camada | Formato | Conteúdo                                            |
| ------ | ------- | --------------------------------------------------- |
| Bronze | JSON    | Resposta bruta da API, preservada por execução      |
| Silver | Parquet | Registros válidos com campos padronizados em inglês |
| Gold   | JSON    | Métricas agregadas dos veículos transformados       |

Os artefatos seguem a convenção:

```text
data/
├── bronze/cars/<run_id>/cars.json
├── silver/cars/<run_id>/cars.parquet
└── gold/cars/<run_id>/cars_metrics.json
```

## Qualidade dos dados

As validações atuais verificam:

- presença de `id`, marca, modelo, ano e preço efetivo;
- ano entre 1900 e 2030;
- preço efetivo maior que zero;
- quilometragem não negativa, quando informada;
- duplicidade de identificadores, por meio de uma função específica de qualidade.

Registros inválidos são separados dos registros válidos antes da transformação.

## Transformação e métricas

A Silver converte os campos da API para um modelo analítico, incluindo `car_id`, `brand`, `model`, `year`, `fuel`, `transmission`, `price_effective`, `price_fipe`, `price_market`, `seller_id` e datas de criação e atualização.

A Gold produz, entre outros indicadores:

- total de veículos;
- distribuição por marca, combustível, câmbio e condição;
- quilometragem média;
- preço efetivo médio;
- diferença média percentual em relação à FIPE;
- visualizações médias.

## Testes

Execute a suíte com:

```bash
python -m pytest -v
```

Os testes cobrem o orquestrador do pipeline, metadados de execução, regras de qualidade, transformação, persistência em JSON/Parquet e cálculos analíticos.

## Estrutura do projeto

```text
src/
├── analytics/       # Cálculo das métricas Gold
├── ingestion/       # Cliente HTTP e extração da API
├── pipeline/        # Orquestração e metadados das execuções
├── quality/         # Validações dos registros
├── storage/         # Persistência e leitura das camadas
└── transformation/  # Padronização dos campos

tests/               # Testes automatizados
data/                # Artefatos Bronze, Silver e Gold
docs/                # Documentação complementar
notebooks/           # Explorações e análises interativas
```

## Observações

- Os dados gerados em `data/` são organizados por execução para manter histórico e permitir auditoria.
- A camada Silver depende de `pandas`, `pyarrow` e do formato Parquet.
- A execução contra a API requer conectividade de rede e uma URL base válida.
