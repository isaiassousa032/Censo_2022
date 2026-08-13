# Contexto do projeto

## Identificação

- **Projeto guarda-chuva:** Censo 2022 — Retratos do Brasil
- **Primeiro módulo:** Alfabetização no Brasil — Censo 2022
- **Subtítulo:** Desigualdades municipais e demográficas entre taxa e contingente populacional

## Objetivo

Analisar como as desigualdades de alfabetização se manifestam entre municípios e grupos demográficos brasileiros, considerando tanto a proporção quanto o número de pessoas não alfabetizadas.

O projeto deverá demonstrar a construção de um produto analítico próprio e reproduzível a partir de dados oficiais, sem se limitar à reprodução de gráficos e resultados disponíveis no portal do IBGE.

## Pergunta central

> Como as desigualdades de alfabetização se manifestam entre os municípios e grupos demográficos brasileiros, considerando tanto a taxa quanto o número de pessoas afetadas?

## Escopo atual

### População de referência

- pessoas residentes no Brasil;
- pessoas com 15 anos ou mais;
- Censo Demográfico 2022.

### Abrangência geográfica

- Brasil;
- Grandes Regiões;
- Unidades da Federação;
- municípios.

### Recortes demográficos

- sexo: homens e mulheres;
- cor ou raça: branca, preta, amarela, parda e indígena;
- grupos de idade: 15 a 19, 20 a 24, 25 a 34, 35 a 44, 45 a 54, 55 a 64 e 65 anos ou mais.

Os recortes demográficos serão analisados inicialmente apenas para Brasil, Grandes Regiões e Unidades da Federação. A análise municipal utilizará os totais demográficos.

## Fora do escopo

Nesta etapa, não serão incluídos:

- população de 5 a 14 anos;
- comparações com o Censo 2010 ou com a PNAD;
- frequência escolar e nível de instrução;
- análises causais ou testes estatísticos sem justificativa;
- recortes territoriais submunicipais;
- tabelas específicas de indígenas ou quilombolas;
- idades individuais ou faixas etárias sobrepostas;
- cruzamentos entre sexo, cor ou raça e idade;
- recortes demográficos municipais;
- classificação arbitrária de prioridade entre municípios;
- Streamlit antes da conclusão do Power BI.

## Fontes oficiais

### SIDRA 9542

- **Endereço:** https://sidra.ibge.gov.br/tabela/9542
- **Finalidade:** fonte principal para os valores absolutos da população total, alfabetizada e não alfabetizada.
- **Observação:** o “percentual do total geral” não representa a taxa de alfabetização.

### SIDRA 9543

- **Endereço:** https://sidra.ibge.gov.br/tabela/9543
- **Finalidade:** fornecer a taxa oficial de alfabetização para validar as taxas calculadas a partir dos valores absolutos da tabela 9542.

## Decisões tomadas

- Os dados brutos deverão permanecer imutáveis.
- Todas as transformações deverão ser documentadas e reproduzíveis.
- Os códigos territoriais oficiais do IBGE serão utilizados como chaves.
- A análise considerará conjuntamente a taxa de não alfabetização e o número de pessoas não alfabetizadas.
- A identidade `não alfabetizadas = total − alfabetizadas` será validada.
- A taxa calculada será validada contra a taxa oficial da tabela 9543.
- Taxas estaduais, regionais e nacional não serão calculadas pela média simples das taxas municipais.
- A taxa de uma população agregada será calculada por `soma das pessoas alfabetizadas ÷ soma da população de referência × 100`.
- Médias e medianas simples das taxas municipais serão usadas apenas para descrever a distribuição dos municípios.
- Outliers não serão removidos automaticamente; o denominador populacional deverá ser considerado.
- A observação de um mapa não será tratada como evidência de clusters estatísticos.
- A categoria indígena representa o quesito de cor ou raça das tabelas selecionadas e não equivale à definição ampliada das divulgações específicas sobre população indígena.
- Novos cruzamentos, tecnologias e estruturas somente serão adicionados quando uma pergunta analítica concreta os justificar.

## Arquitetura atual

Arquitetura aprovada para o desenvolvimento progressivo:

```text
SIDRA / IBGE
↓
Python
↓
Dados brutos
↓
pandas
↓
PostgreSQL local
↓
Power BI
↓
Streamlit posteriormente
```

No estado atual, apenas o versionamento com Git e a documentação inicial foram iniciados. A arquitetura será implementada incrementalmente, conforme as necessidades de cada etapa.

## Status

Estruturação inicial.

## Entregas concluídas

- planejamento formal inicial;
- definição do objetivo, da pergunta central e do escopo;
- seleção das tabelas SIDRA 9542 e 9543;
- aprovação da matriz inicial de extração;
- definição da arquitetura suficiente;
- inicialização do repositório Git local;
- criação da memória operacional do projeto.

## Pendências

- preparar a extração mínima e reproduzível do SIDRA;
- confirmar na API do SIDRA os códigos das variáveis e categorias aprovadas;
- definir o formato e a convenção de nomes dos arquivos brutos;
- criar somente as pastas necessárias para a etapa de extração;
- extrair e preservar os primeiros dados brutos;
- validar valores, categorias, granularidade e cobertura territorial;
- documentar cada decisão à medida que for tomada.

## Próximo passo

Preparar a extração mínima e reproduzível do SIDRA, começando pela identificação e validação dos parâmetros necessários na API antes de escrever o extrator completo.
