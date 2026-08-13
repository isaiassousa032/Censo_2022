# Parâmetros do SIDRA

## Finalidade

Este documento registra os identificadores oficiais necessários para consultar as tabelas SIDRA 9542 e 9543 dentro do escopo aprovado para o módulo **Alfabetização no Brasil — Censo 2022**.

O mapeamento deverá orientar a construção das consultas e evitar:

- uso de variáveis ou categorias fora do escopo;
- confusão entre percentual do total geral e taxa de alfabetização;
- dupla contagem causada por idades individuais ou faixas etárias sobrepostas;
- perda dos códigos territoriais oficiais do IBGE;
- cruzamentos demográficos ainda não justificados por uma pergunta analítica.

## Período

| Código | Referência |
|---:|---|
| 2022 | Censo Demográfico 2022 |

As tabelas 9542 e 9543 possuem, para este estudo, o período de referência 2022.

## Níveis territoriais

| Código | Nível territorial | Uso inicial |
|---|---|---|
| N1 | Brasil | Panorama territorial e recortes demográficos |
| N2 | Grande Região | Panorama territorial e recortes demográficos |
| N3 | Unidade da Federação | Panorama territorial e recortes demográficos |
| N6 | Município | Panorama territorial com totais demográficos |

Os códigos oficiais das localidades deverão ser preservados durante a extração e utilizados como chaves territoriais.

## Tabela 9542

- **Nome:** Pessoas de 15 anos ou mais de idade, total e as alfabetizadas, por sexo, cor ou raça e grupos de idade
- **Endereço:** https://sidra.ibge.gov.br/tabela/9542
- **Finalidade:** fornecer os valores absolutos da população total, alfabetizada e não alfabetizada.

### Variáveis

| Código | Variável | Uso no projeto |
|---:|---|---|
| 950 | Pessoas de 15 anos ou mais de idade | Fonte dos valores absolutos |
| 1000950 | Pessoas de 15 anos ou mais de idade — percentual do total geral | Não utilizar como taxa de alfabetização |

O total, as pessoas alfabetizadas e as pessoas não alfabetizadas são categorias da classificação **Alfabetização**. Elas não constituem três variáveis independentes.

### Classificação: alfabetização

| Código da classificação | Código da categoria | Categoria | Uso inicial |
|---:|---:|---|---|
| 59 | 93024 | Total | Sim |
| 59 | 1023 | Alfabetizadas | Sim |
| 59 | 1024 | Não alfabetizadas | Sim |

### Classificação: sexo

| Código da classificação | Código da categoria | Categoria | Uso inicial |
|---:|---:|---|---|
| 2 | 6794 | Total | Panorama territorial e demais recortes |
| 2 | 4 | Homens | Brasil, Grandes Regiões e UFs |
| 2 | 5 | Mulheres | Brasil, Grandes Regiões e UFs |

### Classificação: cor ou raça

| Código da classificação | Código da categoria | Categoria | Uso inicial |
|---:|---:|---|---|
| 86 | 95251 | Total | Panorama territorial e demais recortes |
| 86 | 2776 | Branca | Brasil, Grandes Regiões e UFs |
| 86 | 2777 | Preta | Brasil, Grandes Regiões e UFs |
| 86 | 2778 | Amarela | Brasil, Grandes Regiões e UFs |
| 86 | 2779 | Parda | Brasil, Grandes Regiões e UFs |
| 86 | 2780 | Indígena | Brasil, Grandes Regiões e UFs |

A categoria indígena representa o quesito de cor ou raça dessas tabelas. Ela não deverá ser interpretada como equivalente à definição ampliada empregada nas divulgações específicas sobre a população indígena.

### Classificação: idade

| Código da classificação | Código da categoria | Categoria | Uso inicial |
|---:|---:|---|---|
| 287 | 100362 | Total | Panorama territorial e demais recortes |
| 287 | 93086 | 15 a 19 anos | Brasil, Grandes Regiões e UFs |
| 287 | 93087 | 20 a 24 anos | Brasil, Grandes Regiões e UFs |
| 287 | 2999 | 25 a 34 anos | Brasil, Grandes Regiões e UFs |
| 287 | 9482 | 35 a 44 anos | Brasil, Grandes Regiões e UFs |
| 287 | 9483 | 45 a 54 anos | Brasil, Grandes Regiões e UFs |
| 287 | 9484 | 55 a 64 anos | Brasil, Grandes Regiões e UFs |
| 287 | 3000 | 65 anos ou mais | Brasil, Grandes Regiões e UFs |

## Tabela 9543

- **Nome:** Taxa de alfabetização das pessoas de 15 anos ou mais de idade por sexo, cor ou raça e grupos de idade
- **Endereço:** https://sidra.ibge.gov.br/tabela/9543
- **Finalidade:** fornecer a taxa oficial de alfabetização para validar as taxas calculadas com os valores absolutos da tabela 9542.

### Variável

| Código | Variável | Uso no projeto |
|---:|---|---|
| 2513 | Taxa de alfabetização das pessoas de 15 anos ou mais de idade | Validação da taxa calculada |

### Classificações

A tabela 9543 utiliza as mesmas classificações e os mesmos códigos de categorias definidos acima para:

- sexo — classificação `2`;
- cor ou raça — classificação `86`;
- idade — classificação `287`.

Ela não possui a classificação Alfabetização (`59`), pois a sua variável já representa diretamente a taxa de alfabetização.

## Categorias excluídas

Não deverão ser selecionadas na extração inicial:

- idades individuais de 15 a 64 anos;
- 75 anos ou mais — código `9486`;
- 80 anos ou mais — código `113623`;
- população de 5 a 14 anos;
- categorias não pertencentes à matriz inicial aprovada;
- cruzamentos entre sexo, cor ou raça e idade;
- recortes demográficos municipais.

As categorias de 75 anos ou mais e 80 anos ou mais estão contidas em 65 anos ou mais. Selecioná-las em conjunto para agregação provocaria sobreposição e poderia gerar dupla contagem.

## Pontos a validar na consulta mínima

A primeira consulta deverá ser pequena e destinada a confirmar o contrato dos dados antes da construção do extrator completo.

Deverão ser verificados:

- período igual a 2022;
- tabela e variável solicitadas;
- nível territorial e código da localidade;
- presença dos códigos territoriais oficiais;
- nomes e códigos das classificações e categorias;
- unidade de medida de cada variável;
- estrutura dos campos retornados;
- quantidade esperada de registros para a granularidade solicitada;
- presença de registros duplicados na granularidade esperada;
- tratamento dos símbolos especiais do SIDRA, como `-`, `0`, `X`, `..` e `...`;
- diferença entre o percentual do total geral da tabela 9542 e a taxa oficial da tabela 9543;
- possibilidade de validar `não alfabetizadas = total − alfabetizadas`;
- possibilidade de validar `taxa de alfabetização = alfabetizadas ÷ total × 100` contra a tabela 9543.

Para isolar problemas de parametrização, a consulta mínima deverá começar pelo Brasil, no período de 2022, com sexo total, cor ou raça total e idade total. Na tabela 9542, deverão ser solicitadas somente a variável de valores absolutos e as três categorias da classificação Alfabetização. A consulta equivalente da tabela 9543 será definida e executada somente após a validação da primeira resposta.
